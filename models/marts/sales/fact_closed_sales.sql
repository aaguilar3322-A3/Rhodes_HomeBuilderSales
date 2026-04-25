{{ config(materialized='table') }}

WITH 
region_closed_sales AS (
    SELECT 
    --date_part('month', CLOSE_DATE) AS Month,
    --date_part('year', CLOSE_DATE) AS Year
    r.*
     FROM {{ ref('regional_manager_closed_sales') }} r
     where IsClosed = 1
)

SELECT * FROM region_closed_sales