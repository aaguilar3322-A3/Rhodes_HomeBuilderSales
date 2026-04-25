{{ config(materialized='table') }}

WITH 
regional_managers AS(
    select distinct
    REGION,
    REGIONAL_MANAGER
    from {{ ref('dim_regional_managers') }}
),
region_sales AS(
    select REGION, avg(TOTAL_DAYS_TO_CLOSE) AVG_DAYS_TO_CLOSE
    from {{ref('regional_manager_closed_sales')}}
    GROUP BY REGION
),
AVG_DAYS_TO_CLOSE AS(
    select

    m.REGION, m.REGIONAL_MANAGER,
    --c.COMMUNITY,
    --s.city, 
    ROUND(s.AVG_DAYS_TO_CLOSE) AVG_DAYS_TO_CLOSE
    from region_sales s
    --LEFT JOIN cities c on s.CITY = c.CITY
    LEFT JOIN regional_managers m on s.REGION = m.REGION
)

select * from AVG_DAYS_TO_CLOSE