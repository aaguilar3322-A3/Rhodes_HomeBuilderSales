{{ config(materialized='table') }}

WITH 
region_sales AS (
    SELECT 
    --date_part('month', CLOSE_DATE) AS Month,
    --date_part('year', CLOSE_DATE) AS Year
    r.*
     FROM {{ ref('v_regional_manager_sales') }} r
)

SELECT * FROM region_sales