select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select state
from "funding_pipeline"."main"."businesses"
where state is null



      
    ) dbt_internal_test