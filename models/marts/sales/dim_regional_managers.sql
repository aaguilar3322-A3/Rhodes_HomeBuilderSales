{{ config(materialized='table') }}

WITH regional_managers AS(
    select DISTINCT
    REGION,
    REGIONAL_MANAGER
    from {{ ref('v_regional_manager_sales') }}
)

select * from regional_managers