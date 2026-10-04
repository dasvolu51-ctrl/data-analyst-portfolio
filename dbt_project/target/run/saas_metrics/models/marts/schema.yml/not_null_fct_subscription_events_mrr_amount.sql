
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select mrr_amount
from "saas_metrics"."main"."fct_subscription_events"
where mrr_amount is null



  
  
      
    ) dbt_internal_test