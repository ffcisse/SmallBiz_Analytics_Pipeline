
    
    

with all_values as (

    select
        status as value_field,
        count(*) as n_records

    from "funding_pipeline"."main"."repayments"
    group by status

)

select *
from all_values
where value_field not in (
    'current','30_days_late','60_days_late','90_days_late','defaulted'
)


