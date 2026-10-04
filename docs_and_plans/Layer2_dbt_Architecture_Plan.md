## Goal Description
This phase implements **Layer 2: Analytics Engineering & Semantic Modeling**. We will transform the cleaned Parquet data into a production-grade Dimensional Star Schema using dbt (Data Build Tool). To guarantee data trust for downstream BI and AI agents, we will enforce strict referential integrity and statistical anomaly detection using `dbt-expectations`. Finally, we will implement the dbt Semantic Layer (MetricFlow) to define core enterprise KPIs (MRR, Active Subscribers, Churn) exclusively in YAML.

## User Review Required
> [!IMPORTANT]
> Please review the proposed Star Schema design and Metric definitions below. Once you click **Proceed**, I will automatically initialize the dbt project, install the `dbt-duckdb` adapter, generate the models, and run the pipeline.

## Proposed Changes

---

### 1. Project Configuration & Dependencies
We will initialize a new dbt project named `saas_metrics` configured to use the **dbt-duckdb** adapter, demonstrating a cutting-edge zero-ETL analytics environment querying Parquet files directly.

#### [NEW] `packages.yml`
```yaml
packages:
  - package: calogica/dbt_expectations
    version: 0.10.4
```
#### [MODIFY] `dbt_project.yml`
Configure materializations (staging as views, dimensional marts as tables) and link to our raw parquet database path.

---

### 2. Staging Layer (Views)
Lightweight views that sit directly on top of our clean Parquet files to alias columns and cast final data types before modeling.
#### [NEW] `models/staging/stg_customers.sql`
#### [NEW] `models/staging/stg_subscriptions.sql`
#### [NEW] `models/staging/stg_billing.sql`
#### [NEW] `models/staging/stg_telemetry.sql`

---

### 3. Dimensional Star Schema (Marts)
The core architecture optimized for high-speed querying and Semantic Layer integration.
#### [NEW] `models/marts/dim_customers.sql`
Contains customer firmographics (Country, Theme, Lang, Signup Date).
#### [NEW] `models/marts/dim_plans.sql`
Contains unique subscription plan tiers derived from the data.
#### [NEW] `models/marts/dim_feature_usage.sql`
Aggregated view of telemetry data per customer (e.g., total logins, total purchases, average session length).
#### [NEW] `models/marts/fct_subscription_events.sql`
A **Monthly Snapshot Fact Table**. It will calculate the active status, current plan, and Monthly Recurring Revenue (MRR) for every customer at the end of every calendar month.

---

### 4. Data Hygiene & Strict Testing
We will enforce primary keys, foreign keys, and anomaly detection bounds to ensure perfect data quality.
#### [NEW] `models/marts/schema.yml`
```yaml
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
              max_value: 100000 # Catch anomalous billing spikes
```

---

### 5. The dbt Semantic Layer (MetricFlow)
We will define our enterprise KPIs directly in YAML. This creates a unified "Semantic Graph" so that any downstream tool queries identical math.
#### [NEW] `models/metrics/semantic_models.yml`
Maps the `fct_subscription_events` table into a semantic model, exposing dimensions (e.g. `country`) and measures (e.g. `mrr_amount`).
#### [NEW] `models/metrics/enterprise_kpis.yml`
```yaml
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
  - name: churn_rate
    description: "Monthly churn rate percentage"
    type: derived
    type_params:
      expr: churned_subscribers / previous_month_active_subscribers
      metrics:
        - name: churned_subscribers
        - name: previous_month_active_subscribers
```

## Verification Plan
Once approved, I will execute the following commands in the terminal to verify the architecture:
### Automated Tests
1. `pip install dbt-duckdb`
2. Execute `dbt deps` to install `dbt-expectations`.
3. Execute `dbt build` to compile the models, run the pipeline, and execute all schema and anomaly tests.

### Manual Verification
You will be able to review the compiled DAG and view the physical parquet files generated in the project directory, confirming the pipeline correctly transitioned your clean data into a Star Schema.
