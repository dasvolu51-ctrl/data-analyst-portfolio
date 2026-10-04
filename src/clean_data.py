import os
import polars as pl
import duckdb

RAW_DIR = r"C:\Users\Public\data_analyst_portfolio\raw_data"
CLEAN_DIR = r"C:\Users\Public\data_analyst_portfolio\clean_data"
os.makedirs(CLEAN_DIR, exist_ok=True)

print("1. Cleaning Customers (Polars Lazy Execution + DuckDB)...")
# Polars Lazy Scan to handle string manipulation efficiently
q_cust = pl.scan_parquet(os.path.join(RAW_DIR, 'customers.parquet'))

q_cust = q_cust.with_columns(
    pl.col('country').str.to_uppercase().str.replace_all(r'\.', '').fill_null('UNKNOWN')
)
q_cust = q_cust.with_columns(
    pl.when(pl.col('country') == 'INDIA').then(pl.lit('IN'))
      .when(pl.col('country') == 'UNITED STATES').then(pl.lit('US'))
      .otherwise(pl.col('country')).alias('country')
)

# Parse corrupted JSON into structured columns
q_cust = q_cust.with_columns([
    pl.col('metadata_json').str.extract(r'"theme":\s*"([^"]+)"', 1).alias('theme'),
    pl.col('metadata_json').str.extract(r'"lang":\s*"([^"]+)"', 1).alias('lang')
]).drop('metadata_json')

# Collect into memory (Backed by Apache Arrow)
df_cust = q_cust.collect()

# Use DuckDB to query the Polars DataFrame directly to utilize its forgiving TRY_CAST for mixed date formats
con = duckdb.connect()
con.execute(f"""
    COPY (
        SELECT 
            customer_id, email, country,
            TRY_CAST(signup_date AS TIMESTAMP) AS signup_date,
            theme, lang
        FROM df_cust
    ) TO '{CLEAN_DIR}/customers_clean.parquet' (FORMAT PARQUET);
""")
print("Clean Customers saved.")

print("2. Cleaning Subscriptions (Enforcing Referential Integrity)...")
q_subs = pl.scan_parquet(os.path.join(RAW_DIR, 'subscriptions.parquet'))
q_subs = q_subs.with_columns([
    pl.col('plan_name').str.to_uppercase().str.strip_chars(),
    pl.col('status').str.to_titlecase().str.strip_chars(),
])

# Enforce Referential Integrity (Inner Join with Clean Customers)
q_subs_clean = q_subs.join(q_cust.select('customer_id'), on='customer_id', how='inner')
df_subs = q_subs_clean.collect()

con.execute(f"""
    COPY (
        SELECT 
            sub_id, customer_id, plan_name, status,
            TRY_CAST(start_date AS TIMESTAMP) AS start_date
        FROM df_subs
    ) TO '{CLEAN_DIR}/subscriptions_clean.parquet' (FORMAT PARQUET);
""")
print("Clean Subscriptions saved.")

print("3. Cleaning Billing (DuckDB Zero-ETL Querying & String Parsing)...")
# DuckDB directly querying the raw Parquet chunks
con.execute(f"""
    COPY (
        SELECT 
            b.invoice_id, 
            b.sub_id,
            -- Clean amounts: remove 'USD ', change ',' to '.', cast to DOUBLE
            TRY_CAST(REPLACE(REPLACE(b.amount, 'USD ', ''), ',', '.') AS DOUBLE) AS amount,
            -- Clean mixed date formats
            TRY_CAST(b.billing_date AS TIMESTAMP) AS billing_date,
            UPPER(TRIM(b.payment_status)) AS payment_status
        FROM read_parquet('{RAW_DIR}/billing_part_*.parquet') b
        -- Inner Join to drop orphaned records (Referential Integrity)
        INNER JOIN read_parquet('{CLEAN_DIR}/subscriptions_clean.parquet') s ON b.sub_id = s.sub_id
        WHERE TRY_CAST(REPLACE(REPLACE(b.amount, 'USD ', ''), ',', '.') AS DOUBLE) >= 0
    ) TO '{CLEAN_DIR}/billing_clean.parquet' (FORMAT PARQUET);
""")
print("Clean Billing saved.")

print("4. Cleaning Telemetry (Filtering extreme outliers & nulls)...")
con.execute(f"""
    COPY (
        SELECT 
            t.event_id, 
            t.customer_id, 
            TRIM(LOWER(t.event_type)) AS event_type,
            TRY_CAST(t.timestamp AS TIMESTAMP) AS timestamp,
            TRY_CAST(NULLIF(NULLIF(t.session_length_sec, 'null'), 'NaN') AS INT) AS session_length_sec,
            UPPER(TRIM(t.device_os)) AS device_os
        FROM read_parquet('{RAW_DIR}/telemetry_part_*.parquet') t
        -- Inner Join to drop orphaned records
        INNER JOIN read_parquet('{CLEAN_DIR}/customers_clean.parquet') c ON t.customer_id = c.customer_id
        -- Filter out negative or impossible session lengths
        WHERE TRY_CAST(NULLIF(NULLIF(t.session_length_sec, 'null'), 'NaN') AS INT) BETWEEN 0 AND 86400
    ) TO '{CLEAN_DIR}/telemetry_clean.parquet' (FORMAT PARQUET);
""")
print("Clean Telemetry saved.")

print("5. Generating the 1,000-Row Clean Joined Sample...")
con.execute(f"""
    COPY (
        SELECT 
            t.event_id, t.customer_id, t.event_type, t.timestamp, t.session_length_sec, t.device_os,
            c.email, c.country, c.signup_date, c.theme, c.lang,
            s.sub_id, s.plan_name, s.status AS sub_status, s.start_date,
            b.invoice_id, b.amount, b.billing_date, b.payment_status
        FROM read_parquet('{CLEAN_DIR}/telemetry_clean.parquet') t
        LEFT JOIN read_parquet('{CLEAN_DIR}/customers_clean.parquet') c ON t.customer_id = c.customer_id
        LEFT JOIN read_parquet('{CLEAN_DIR}/subscriptions_clean.parquet') s ON c.customer_id = s.customer_id
        LEFT JOIN read_parquet('{CLEAN_DIR}/billing_clean.parquet') b ON s.sub_id = b.sub_id
        LIMIT 1000
    ) TO '{CLEAN_DIR}/clean_sample_1000.csv' (HEADER, DELIMITER ',');
""")
print("Clean sample created successfully.")
print("All cleaning tasks successfully completed! Clean Data is ready.")
