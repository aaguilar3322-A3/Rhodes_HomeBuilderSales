{{ config(materialized='table') }}

WITH dim_close_date_my AS(
    select DISTINCT
    --date_part('month', CLOSE_DATE) AS Month,
    --date_part('year', CLOSE_DATE) AS Year
    s.Month,
    s.Year
    from {{ ref('regional_manager_sales') }} s
)

select * from dim_close_date_my