
    

    create  table
      "saas_metrics"."main"."dim_customers__dbt_tmp"
  
    
    as (
      SELECT customer_id, email, country, signup_date, theme, lang 
FROM "saas_metrics"."main"."stg_customers"
    );
    
  