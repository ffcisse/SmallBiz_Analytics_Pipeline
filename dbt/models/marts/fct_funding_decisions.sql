{{
    config(
        materialized='table',
        schema='marts',
        indexes=[
            {'columns': ['business_id']},
            {'columns': ['funding_id']},
            {'columns': ['decision_date']}
        ]
    )
}}

with funding as (
    select * from {{ ref('stg_funding_decisions') }}
),

businesses as (
    select * from {{ ref('stg_businesses') }}
),

repayments as (
    select 
        funding_id,
        status,
        is_defaulted,
        last_payment_date,
        total_paid
    from {{ ref('stg_repayments') }}
)

select
    f.funding_id,
    f.business_id,
    b.business_name,
    b.industry,
    b.state,
    b.employee_count,
    b.annual_revenue,
    f.funding_amount,
    f.decision,
    f.is_approved,
    f.interest_rate,
    f.decision_date,
    r.status as repayment_status,
    r.is_defaulted,
    r.last_payment_date,
    r.total_paid,
    datediff('day', f.decision_date, current_date()) as days_since_funding,
    case 
        when r.is_defaulted = 1 then 'High Risk'
        when r.status in ('90_days_late', '60_days_late') then 'Medium Risk'
        when r.status = '30_days_late' then 'Low Risk'
        else 'Current'
    end as risk_segment,
    now() as dbt_loaded_at
from funding f
left join businesses b on f.business_id = b.business_id
left join repayments r on f.funding_id = r.funding_id
