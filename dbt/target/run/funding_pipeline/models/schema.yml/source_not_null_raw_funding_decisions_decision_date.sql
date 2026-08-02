select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select decision_date
from "funding_pipeline"."main"."funding_decisions"
where decision_date is null



      
    ) dbt_internal_test