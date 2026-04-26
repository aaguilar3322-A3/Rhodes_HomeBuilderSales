{{ config(materialized='table') }}

WITH 
region_sales AS(

        select
         s.Year, s.Month, region, regional_manager
        ,SUM(isclosed) AS Total_Closed
        ,SUM(isundercontract) AS Total_Under_Contract
        ,SUM(iscancelled) AS Total_Cancelled
        ,round(avg(Contract_Price)) AS Average_Contract_Price
        ,COUNT(CONTRACT_ID) AS Total_Contracts
        from {{ ref('regional_manager_sales') }} s
        GROUP BY s.Year, s.Month, region, regional_manager

)

select * from region_sales