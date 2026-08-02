select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select funding_amount
from "funding_pipeline"."main"."funding_decisions"
where funding_amount is null



      
    ) dbt_internal_test