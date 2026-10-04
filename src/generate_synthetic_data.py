import os
import numpy as np
import pandas as pd
import random
import json

# Constants
OUTPUT_DIR = r"C:\Users\Public\data_analyst_portfolio\raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NUM_CUSTOMERS = 1_000_000
NUM_SUBS = 1_500_000
NUM_BILLING = 2_500_000
NUM_TELEMETRY = 5_000_000

print("Generating Customers (1M rows)...")
customer_ids = np.arange(1, NUM_CUSTOMERS + 1)

def random_dates(start_str, end_str, n, messy=True):
    start = pd.to_datetime(start_str).value // 10**9
    end = pd.to_datetime(end_str).value // 10**9
    times = np.random.randint(start, end, n)
    dates = pd.to_datetime(times, unit='s')
    if not messy:
        return dates.astype(str)
    
    str_dates = []
    for d in dates:
        r = random.random()
        if r < 0.2:
            str_dates.append(d.strftime("%m/%d/%Y")) # US
        elif r < 0.4:
            str_dates.append(d.strftime("%d-%m-%Y")) # EU
        elif r < 0.6:
            str_dates.append(d.strftime("%Y/%m/%d %H:%M:%S"))
        elif r < 0.65:
            str_dates.append(None) # Null
        else:
            str_dates.append(d.isoformat())
    return str_dates

# 1. Customers Table
customers = pd.DataFrame({
    'customer_id': customer_ids,
    'email': [f"user{i}@example.com" if random.random() > 0.05 else f"USER{i}@@example..com" for i in range(NUM_CUSTOMERS)],
    'country': np.random.choice(['US', 'UK', 'CA', 'India', 'IN', 'U.S.', 'Canada', 'uk', None], NUM_CUSTOMERS),
    'signup_date': random_dates('2020-01-01', '2025-12-31', NUM_CUSTOMERS, messy=True)
})

# Inject corrupted JSON
def generate_json(i):
    if random.random() < 0.1:
        return '{"theme": "dark", "lang"' # corrupted missing bracket
    return json.dumps({"theme": random.choice(["dark", "light"]), "lang": random.choice(["en", "es", "fr"])})

customers['metadata_json'] = [generate_json(i) for i in range(NUM_CUSTOMERS)]
customers.to_parquet(os.path.join(OUTPUT_DIR, 'customers.parquet'), index=False)
print("Customers saved.")

# 2. Subscriptions Table
print("Generating Subscriptions (1.5M rows)...")
subs = pd.DataFrame({
    'sub_id': np.arange(1, NUM_SUBS + 1),
    'customer_id': np.random.choice(customer_ids, NUM_SUBS),
    'plan_name': np.random.choice(['Basic', 'Pro', 'Enterprise', 'basic ', 'PRO', '  Enterprise'], NUM_SUBS),
    'status': np.random.choice(['Active', 'Canceled', 'Past Due', 'active', None], NUM_SUBS),
    'start_date': random_dates('2021-01-01', '2025-12-31', NUM_SUBS, messy=True)
})
# Inject orphaned foreign keys
mask = np.random.random(NUM_SUBS) < 0.05
subs.loc[mask, 'customer_id'] = np.random.randint(NUM_CUSTOMERS + 100000, NUM_CUSTOMERS + 200000, sum(mask))
subs.to_parquet(os.path.join(OUTPUT_DIR, 'subscriptions.parquet'), index=False)
print("Subscriptions saved.")

# 3. Billing Table
print("Generating Billing (2.5M rows in chunks)...")
for chunk_idx in range(5):
    chunk_size = NUM_BILLING // 5
    billing = pd.DataFrame({
        'invoice_id': np.arange(chunk_idx*chunk_size + 1, (chunk_idx+1)*chunk_size + 1),
        'sub_id': np.random.randint(1, NUM_SUBS + 50000, chunk_size), # Some orphaned
        'amount': np.random.choice(['19.99', '49.99', '199.99', '19,99', 'USD 49.99', 'NaN', '-10.0'], chunk_size),
        'billing_date': random_dates('2021-01-01', '2025-12-31', chunk_size, messy=True),
        'payment_status': np.random.choice(['Paid', 'Failed', 'Pending', 'paid', 'FAILED', None], chunk_size)
    })
    billing.to_parquet(os.path.join(OUTPUT_DIR, f'billing_part_{chunk_idx+1}.parquet'), index=False)
print("Billing saved.")

# 4. Telemetry Table
print("Generating Telemetry (5M rows in chunks)...")
for chunk_idx in range(5):
    chunk_size = NUM_TELEMETRY // 5
    telemetry = pd.DataFrame({
        'event_id': np.arange(chunk_idx*chunk_size + 1, (chunk_idx+1)*chunk_size + 1),
        'customer_id': np.random.choice(customer_ids, chunk_size),
        'event_type': np.random.choice(['login', 'logout', 'view_item', 'purchase', 'error', 'LOGIN ', 'ViewItem'], chunk_size),
        'timestamp': random_dates('2023-01-01', '2025-12-31', chunk_size, messy=True),
        'session_length_sec': np.random.choice(['10', '120', '300', '-50', '99999', 'null', 'NaN'], chunk_size),
        'device_os': np.random.choice(['iOS', 'Android', 'Windows', 'Mac', 'ios', 'android', None], chunk_size)
    })
    telemetry.to_parquet(os.path.join(OUTPUT_DIR, f'telemetry_part_{chunk_idx+1}.parquet'), index=False)
    
    if chunk_idx == 0:
        telemetry_sample = telemetry.sample(1000).copy()
print("Telemetry saved.")

# 5. The 1,000-Row Joined Messy Sample
print("Generating Merged Messy Sample (1,000 rows)...")
billing_sample = pd.read_parquet(os.path.join(OUTPUT_DIR, 'billing_part_1.parquet')).sample(5000)

sample_merged = telemetry_sample.merge(customers, on='customer_id', how='left', suffixes=('_tel', '_cust'))
sample_merged = sample_merged.merge(subs.drop_duplicates(subset=['customer_id']), on='customer_id', how='left')
sample_merged = sample_merged.merge(billing_sample.drop_duplicates(subset=['sub_id']), on='sub_id', how='left')

sample_csv_path = os.path.join(OUTPUT_DIR, 'messy_sample_1000.csv')
sample_merged.to_csv(sample_csv_path, index=False)
print(f"Sample saved to {sample_csv_path}")

print("All tasks successfully completed! Data is ready for DuckDB/Polars.")
