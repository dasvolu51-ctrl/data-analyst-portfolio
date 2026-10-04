
  
  create view "saas_metrics"."main"."stg_subscriptions__dbt_tmp" as (
    SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/subscriptions_clean.parquet')
  );
