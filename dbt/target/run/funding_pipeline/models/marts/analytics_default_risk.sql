
  
    
    

    create  table
      "funding_pipeline"."main_marts"."analytics_default_risk__dbt_tmp"
  
    as (
      

with funding_data as (
    select * from "funding_pipeline"."main_marts"."fct_funding_decisions"
)

select
    industry,
    state,
    risk_segment,
    count(*) as total_fundings,
    sum(case when is_approved = 1 then 1 else 0 end) as approved_count,
    sum(case when is_defaulted = 1 then 1 else 0 end) as defaulted_count,
    round(100.0 * sum(case when is_defaulted = 1 then 1 else 0 end) / count(*), 2) as default_rate_pct,
    round(avg(funding_amount), 2) as avg_funding_amount,
    round(avg(days_since_funding), 0) as avg_days_funded,
    now() as dbt_loaded_at
from funding_data
group by industry, state, risk_segment
order by default_rate_pct desc
    );
  
  