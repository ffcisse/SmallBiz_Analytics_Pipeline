
    
    

select
    funding_id as unique_field,
    count(*) as n_records

from "funding_pipeline"."main"."funding_decisions"
where funding_id is not null
group by funding_id
having count(*) > 1


