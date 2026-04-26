{{ config(materialized='table') }}

WITH dim_close_dates AS(
    select DISTINCT
    CLOSE_DATE
    from {{ ref('v_regional_manager_sales') }}
    where CLOSE_DATE IS NOT NULL
)

select * from dim_close_dates