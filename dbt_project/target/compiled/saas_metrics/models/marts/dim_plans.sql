SELECT DISTINCT plan_name 
FROM "saas_metrics"."main"."stg_subscriptions"
WHERE plan_name IS NOT NULL