select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    funding_id as unique_field,
    count(*) as n_records

from "funding_pipeline"."main"."funding_decisions"
where funding_id is not null
group by funding_id
having count(*) > 1



      
    ) dbt_internal_test