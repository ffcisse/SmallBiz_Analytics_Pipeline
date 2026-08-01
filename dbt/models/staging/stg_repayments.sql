{{
    config(
        materialized='view',
        schema='staging'
    )
}}

with source_data as (
    select
        repayment_id,
        funding_id,
        business_id,
        status,
        last_payment_date,
        total_paid,
        created_at
    from {{ source('raw', 'repayments') }}
)

select
    repayment_id,
    funding_id,
    business_id,
    status,
    cast(last_payment_date as date) as last_payment_date,
    cast(total_paid as decimal(15, 2)) as total_paid,
    case 
        when status = 'current' then 0
        when status = 'defaulted' then 1
        else 0
    end as is_defaulted,
    cast(created_at as timestamp) as created_at,
    current_timestamp() as dbt_loaded_at
from source_data
