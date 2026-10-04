
    

    create  table
      "saas_metrics"."main"."fct_subscription_events__dbt_tmp"
  
    
    as (
      WITH monthly_billing AS (
    SELECT 
        sub_id, 
        DATE_TRUNC('month', billing_date) AS billing_month,
        SUM(amount) AS mrr_amount
    FROM "saas_metrics"."main"."stg_billing"
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
FROM "saas_metrics"."main"."stg_subscriptions" s
JOIN monthly_billing b ON s.sub_id = b.sub_id
    );
    
  