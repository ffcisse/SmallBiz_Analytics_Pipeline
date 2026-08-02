
    
    

select
    business_id as unique_field,
    count(*) as n_records

from "funding_pipeline"."main"."businesses"
where business_id is not null
group by business_id
having count(*) > 1


