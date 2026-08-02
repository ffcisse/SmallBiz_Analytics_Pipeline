{{
    config(
        materialized='table',
        schema='marts'
    )
}}

with funding_data as (
    select * from {{ ref('fct_funding_decisions') }}
)

select
    date_trunc('month', funding_data.decision_date) as cohort_month,
    industry,
    count(*) as total_fundings,
    sum(case when decision = 'approved' then 1 else 0 end) as approved_count,
    sum(case when decision = 'denied' then 1 else 0 end) as denied_count,
    round(100.0 * sum(case when decision = 'approved' then 1 else 0 end) / count(*), 2) as approval_rate_pct,
    sum(case when is_defaulted = 1 then 1 else 0 end) as default_count,
    round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / 
          nullif(sum(case when decision = 'approved' then 1 else 0 end), 0), 2) as cohort_default_rate_pct,
    round(avg(funding_amount), 0) as avg_funding_amount,
    now() as dbt_loaded_at
from funding_data
group by date_trunc('month', funding_data.decision_date), industry
order by cohort_month desc, industry
