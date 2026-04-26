{{ config(materialized='table') }}

WITH 
region_sales AS(
    SELECT
    DENSE_RANK() OVER (ORDER BY SALES_TARGET_PCT DESC) SALES_TARGET_Rank
    , sc.*
    FROM(
        select
        region, regional_manager, rm_sales_target_units
        , rm_margin_target_pct
        ,SUM(isclosed) AS Total_Closed
        ,SUM(isundercontract) AS Total_Under_Contract
        ,SUM(iscancelled) AS Total_Cancelled
        ,ROUND(((SUM(isclosed) / rm_sales_target_units))*100) SALES_TARGET_PCT
        ,round(avg(Contract_Price)) AS Average_Contract_Price
        ,COUNT(CONTRACT_ID) AS Total_Contracts
        ,((SUM(isclosed) / COUNT(CONTRACT_ID)) * 100) AS ClosedPercent
       from {{ ref('regional_manager_sales') }} r
        GROUP BY region, regional_manager, rm_sales_target_units, rm_margin_target_pct
    ) sc
)

select * from region_sales