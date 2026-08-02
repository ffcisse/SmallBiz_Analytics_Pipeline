select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        industry as value_field,
        count(*) as n_records

    from "funding_pipeline"."main"."businesses"
    group by industry

)

select *
from all_values
where value_field not in (
    'Technology','Retail','Healthcare','Finance','Manufacturing','Hospitality','Education','Construction','Real Estate','Transportation'
)



      
    ) dbt_internal_test