{{ config(materialized='table') }}

WITH cities AS(
    select distinct
    COMMUNITY,
    CITY,
    REGION
    from {{ ref('dim_cities') }}
),
regional_managers AS(
    select distinct
    REGION,
    REGIONAL_MANAGER
    from {{ ref('dim_regional_managers') }}
),
region_sales AS(
    select REGION, avg(CONTRACT_PRICE) AVG_SALESPRICE_PER_REGION
    from {{ref('regional_manager_closed_sales')}}
    GROUP BY REGION
),
close_date_MY AS(
    select distinct
    d.Year,
    d.month
    from {{ ref('dim_close_date_my') }} d
),
avg_sales_per_region AS(
    select

    m.REGION, m.REGIONAL_MANAGER,
    --c.COMMUNITY,
    --s.city, 
    s.AVG_SALESPRICE_PER_REGION
    from region_sales s
    --LEFT JOIN cities c on s.CITY = c.CITY
    LEFT JOIN regional_managers m on s.REGION = m.REGION
)

select * from avg_sales_per_region