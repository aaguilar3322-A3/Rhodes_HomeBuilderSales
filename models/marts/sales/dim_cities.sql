{{ config(materialized='table') }}

WITH dim_cities AS(
    select DISTINCT
    REGION,
    CITY
    from {{ ref('regional_manager_sales') }}
)

select * from dim_cities