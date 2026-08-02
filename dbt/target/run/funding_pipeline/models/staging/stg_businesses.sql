
  
  create view "funding_pipeline"."main_staging"."stg_businesses__dbt_tmp" as (
    

with source_data as (
    select
        business_id,
        business_name,
        industry,
        state,
        founded_date,
        employee_count,
        annual_revenue,
        created_at
    from "funding_pipeline"."main"."businesses"
)

select
    business_id,
    business_name,
    industry,
    state,
    cast(founded_date as date) as founded_date,
    employee_count,
    annual_revenue,
    cast(created_at as timestamp) as created_at,
    now() as dbt_loaded_at
from source_data
  );
