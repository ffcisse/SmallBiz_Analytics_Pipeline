select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select repayment_id
from "funding_pipeline"."main"."repayments"
where repayment_id is null



      
    ) dbt_internal_test