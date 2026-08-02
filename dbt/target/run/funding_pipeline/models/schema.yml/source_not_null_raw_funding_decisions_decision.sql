select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select decision
from "funding_pipeline"."main"."funding_decisions"
where decision is null



      
    ) dbt_internal_test