
    
    

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


