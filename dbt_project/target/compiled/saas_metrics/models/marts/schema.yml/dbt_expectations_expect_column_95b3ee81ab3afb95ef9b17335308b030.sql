






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and mrr_amount >= 0 and mrr_amount <= 100000
)
 as expression


    from "saas_metrics"."main"."fct_subscription_events"
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







