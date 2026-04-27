{{ config(materialized='table') }}

WITH 
sales_consultant_closed_sales AS(
    SELECT
    DENSE_RANK() OVER (ORDER BY Total_Closed DESC) Total_Closing_Rank
    , sc.*
    FROM(
        select
        sales_consultant
        ,round(avg(agent_commission)) AS Total_Average_Commission
        ,SUM(isclosed) AS Total_Closed
        ,SUM(isundercontract) AS Total_Under_Contract
        ,SUM(iscancelled) AS Total_Cancelled
        ,COUNT(CONTRACT_ID) AS Total_Contracts
        ,((SUM(isclosed) / COUNT(CONTRACT_ID)) * 100) AS Total_Closed_Pct
        from {{ ref('v_regional_manager_sales') }} r
        GROUP BY sales_consultant
    ) sc
)

select * from sales_consultant_closed_sales