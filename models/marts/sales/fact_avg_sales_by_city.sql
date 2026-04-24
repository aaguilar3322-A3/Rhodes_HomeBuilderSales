{{ config(materialized='table') }}

WITH cities AS(
    select
    COMMUNITY,
    CITY,
    REGION
    from {{ ref('dim_cities') }}
),
regional_managers AS(
    select
    REGION,
    REGIONAL_MANAGER
    from {{ ref('dim_regional_managers') }}
),
regional_sales AS(
    select CITY, (SUM(s.CONTRACT_PRICE) / SUM(s.SQFT)) AS PRICE_PER_SQFT,
    from {{ref('regional_manager_sales')}}
    GROUP BY CITY
)

select *
from regional_sales s
LEFT JOIN cities c on s.CITY = c.CITY
LEFT JOIN regional_managers m on c.REGION = m.REGION