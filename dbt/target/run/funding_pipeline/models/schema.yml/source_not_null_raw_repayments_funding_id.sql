select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select funding_id
from "funding_pipeline"."main"."repayments"
where funding_id is null



      
    ) dbt_internal_test