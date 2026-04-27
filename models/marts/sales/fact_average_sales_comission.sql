{{ config(materialized='table') }}


WITH 
sales_consultant_closed_sales AS(
    SELECT
    DENSE_RANK() OVER (ORDER BY Total_Closed DESC) Closing_Rank
    , sc.*
    FROM(
        select
        round(avg(agent_commission)) AS Average_Commission
        ,SUM(isclosed) AS Total_Closed
        ,COUNT(CONTRACT_ID) AS Total_Contracts
        ,((SUM(isclosed) / COUNT(CONTRACT_ID)) * 100) AS ClosedPercent
        from {{ ref('v_regional_manager_closed_sales') }} r
    ) sc
)

select * from sales_consultant_closed_sales