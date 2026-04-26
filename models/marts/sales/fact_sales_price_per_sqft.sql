
{{ config(materialized='table') }}

WITH price_persq_sales AS(
    select
    r.YEAR,
    r.MONTH,
    r.COMMUNITY,
    r.CITY,
    r.REGION,
    r.REGIONAL_MANAGER,
    r.PLAN_NAME,
    r.BUYER_SOURCE,
    r.LOAN_TYPE,
    r.SALES_CONSULTANT,
    r.PRICE_PER_SQFT
    from {{ ref('v_regional_manager_sales') }} r
)

select * from price_persq_sales
