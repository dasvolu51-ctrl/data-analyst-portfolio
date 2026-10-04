
  
  create view "saas_metrics"."main"."stg_customers__dbt_tmp" as (
    SELECT * FROM read_parquet('C:/Users/Public/data_analyst_portfolio/clean_data/customers_clean.parquet')
  );
