select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select industry
from "funding_pipeline"."main"."businesses"
where industry is null



      
    ) dbt_internal_test