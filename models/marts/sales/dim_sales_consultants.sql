{{ config(materialized='table') }}

WITH dim_sales_consultants AS(
    select DISTINCT
    SALES_CONSULTANT
    from {{ ref('regional_manager_sales') }}
)

select * from dim_sales_consultants