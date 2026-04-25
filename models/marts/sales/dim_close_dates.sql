{{ config(materialized='table') }}

WITH dim_close_dates AS(
    select DISTINCT
    CLOSE_DATE
    from {{ ref('regional_manager_sales') }}
)

select * from dim_close_dates