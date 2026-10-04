SELECT DISTINCT plan_name 
FROM {{ ref('stg_subscriptions') }}
WHERE plan_name IS NOT NULL