select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select employee_count
from "funding_pipeline"."main"."businesses"
where employee_count is null



      
    ) dbt_internal_test