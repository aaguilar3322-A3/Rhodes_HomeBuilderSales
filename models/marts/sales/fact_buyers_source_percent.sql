{{ config(materialized='table') }}


WITH 
Buyer_Source_sales AS(
    SELECT
    DENSE_RANK() OVER (ORDER BY Total_Closed DESC) Total_Closed_Rank
    , sc.*
    FROM(
        select
        BUYER_SOURCE
        ,SUM(isclosed) AS Total_Closed
        ,SUM(isundercontract) AS Total_Under_Contract
        ,SUM(iscancelled) AS Total_Cancelled
        ,round(avg(Contract_Price)) AS Average_Contract_Price
        ,COUNT(CONTRACT_ID) AS Total_Contracts
        ,((SUM(isclosed) / COUNT(CONTRACT_ID)) * 100) AS ClosedPercent
        from {{ ref('regional_manager_sales') }} r
        GROUP BY BUYER_SOURCE
    ) sc
)

select * from Buyer_Source_sales