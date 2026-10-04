import os

base_dir = r"C:\Users\Public\data_analyst_portfolio\stars_schema"
dirs = [
    "models/staging",
    "models/marts",
    "models/metrics"
]
for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {
    "profiles.yml": """
saas_metrics:
  outputs:
    dev:
      type: duckdb
      path: saas_metrics.duckdb
      threads: 4
  target: dev
""",
    "dbt_project.yml": """
name: 'saas_metrics'
version: '1.0.0'
config-version: 2
profile: 'saas_metrics'
model-paths: ["models"]
clean-targets: ["target", "dbt_packages"]
models:
  saas_metrics:
    staging:
      +materialized: view
    marts:
      +materialized: table
""",
    "packages.yml": """
packages:
  - package: calogica/dbt_expectations
    version: 0.10.4
""",
    "models/staging/stg_customers.sql": """
SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/customers_clean.parquet')
""",
    "models/staging/stg_subscriptions.sql": """
SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/subscriptions_clean.parquet')
""",
    "models/staging/stg_billing.sql": """
SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/billing_clean.parquet')
""",
    "models/staging/stg_telemetry.sql": """
SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/telemetry_clean.parquet')
""",
    "models/marts/dim_customers.sql": """
SELECT customer_id, email, country, signup_date, theme, lang 
FROM {{ ref('stg_customers') }}
""",
    "models/marts/dim_plans.sql": """
SELECT DISTINCT plan_name 
FROM {{ ref('stg_subscriptions') }}
WHERE plan_name IS NOT NULL
""",
    "models/marts/dim_feature_usage.sql": """
SELECT 
    customer_id, 
    COUNT(event_id) as total_events, 
    SUM(session_length_sec) as total_session_time 
FROM {{ ref('stg_telemetry') }} 
GROUP BY customer_id
""",
    "models/marts/fct_subscription_events.sql": """
WITH monthly_billing AS (
    SELECT 
        sub_id, 
        DATE_TRUNC('month', billing_date) AS billing_month,
        SUM(amount) AS mrr_amount
    FROM {{ ref('stg_billing') }}
    WHERE payment_status = 'Paid'
    GROUP BY 1, 2
)
SELECT 
    s.customer_id,
    s.sub_id,
    b.billing_month AS snapshot_month,
    s.plan_name,
    s.status AS current_status,
    b.mrr_amount
FROM {{ ref('stg_subscriptions') }} s
JOIN monthly_billing b ON s.sub_id = b.sub_id
""",
    "models/marts/schema.yml": """
version: 2
models:
  - name: fct_subscription_events
    columns:
      - name: customer_id
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: mrr_amount
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000
""",
    "models/metrics/semantic_models.yml": """
semantic_models:
  - name: subscription_events
    model: ref('fct_subscription_events')
    defaults:
      agg_time_dimension: snapshot_month
    entities:
      - name: customer
        type: foreign
        expr: customer_id
      - name: subscription
        type: primary
        expr: sub_id
    dimensions:
      - name: snapshot_month
        type: time
        type_params:
          time_granularity: month
      - name: plan_name
        type: categorical
    measures:
      - name: mrr_amount
        expr: mrr_amount
        agg: sum
      - name: active_subscriber_count
        expr: customer_id
        agg: count_distinct
""",
    "models/metrics/enterprise_kpis.yml": """
metrics:
  - name: mrr
    description: "Monthly Recurring Revenue"
    type: simple
    type_params:
      measure: mrr_amount
  - name: active_subscribers
    description: "Count of distinct active subscribers"
    type: simple
    type_params:
      measure: active_subscriber_count
"""
}

for filepath, content in files.items():
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
print(f"dbt project successfully generated in {base_dir}")
