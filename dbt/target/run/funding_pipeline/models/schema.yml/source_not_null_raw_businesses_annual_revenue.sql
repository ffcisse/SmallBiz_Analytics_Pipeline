select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select annual_revenue
from "funding_pipeline"."main"."businesses"
where annual_revenue is null



      
    ) dbt_internal_test