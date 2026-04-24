
{{ config(materialized='table') }}

WITH price_persq_sales AS(
    select
    COMMUNITY,
    CITY,
    REGION,
    REGIONAL_MANAGER,
    PLAN_NAME,
    BUYER_SOURCE,
    LOAN_TYPE,
    SALES_CONSULTANT,
    PRICE_PER_SQFT
    from {{ ref('regional_manager_sales') }}
)

select * from price_persq_sales
