select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select business_name
from "funding_pipeline"."main"."businesses"
where business_name is null



      
    ) dbt_internal_test