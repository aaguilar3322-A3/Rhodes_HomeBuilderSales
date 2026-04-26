{{ config(materialized='table') }}

WITH dim_cities AS(
    select DISTINCT
    COMMUNITY,
    REGION,
    CITY
    from {{ ref('v_regional_manager_sales') }}
)

select * from dim_cities