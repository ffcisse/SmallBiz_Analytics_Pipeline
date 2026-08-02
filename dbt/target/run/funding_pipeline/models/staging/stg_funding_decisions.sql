
  
  create view "funding_pipeline"."main_staging"."stg_funding_decisions__dbt_tmp" as (
    

with source_data as (
    select
        funding_id,
        business_id,
        funding_amount,
        decision,
        decision_date,
        interest_rate,
        created_at
    from "funding_pipeline"."main"."funding_decisions"
)

select
    funding_id,
    business_id,
    cast(funding_amount as decimal(15, 2)) as funding_amount,
    decision,
    cast(decision_date as date) as decision_date,
    cast(interest_rate as decimal(6, 4)) as interest_rate,
    case when decision = 'approved' then 1 else 0 end as is_approved,
    cast(created_at as timestamp) as created_at,
    now() as dbt_loaded_at
from source_data
  );
