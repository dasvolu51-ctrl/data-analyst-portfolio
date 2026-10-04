
    

    create  table
      "saas_metrics"."main"."metricflow_time_spine__dbt_tmp"
  
    
    as (
      

select CAST(range AS DATE) as date_day
from range(DATE '2020-01-01', DATE '2030-01-01', INTERVAL 1 DAY)
    );
    
  