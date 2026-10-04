SELECT customer_id, email, country, signup_date, theme, lang 
FROM {{ ref('stg_customers') }}