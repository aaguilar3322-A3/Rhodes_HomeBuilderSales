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
city_sales AS(
    select CITY, avg(CONTRACT_PRICE) AVG_SALESPRICE_PER_CITY
    from {{ref('regional_manager_sales')}}
    GROUP BY CITY
),
avg_sales_per_city AS(
    select
    m.REGION, m.REGIONAL_MANAGER,
    c.COMMUNITY,
    s.city, s.AVG_SALESPRICE_PER_CITY
    from city_sales s
    LEFT JOIN cities c on s.CITY = c.CITY
    LEFT JOIN regional_managers m on c.REGION = m.REGION
)

select * from avg_sales_per_city