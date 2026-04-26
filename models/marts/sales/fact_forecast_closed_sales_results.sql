{{ config(materialized='table') }}

WITH V_CLOSED_SALES_MONTHLY AS(
    SELECT
        REGION,
        MONTH_DATE,
        TOTAL_CLOSED AS ACTUAL,
        NULL AS FORECAST,
        NULL AS LOWER_BOUND,
        NULL AS UPPER_BOUND
    FROM STAGING_SALES.V_CLOSED_SALES_MONTHLY
),
FORECAST_CLOSED_SALES_RESULTS AS(
        SELECT
        REPLACE(series, '"', '') AS REGION,
        ts AS MONTH_DATE,
        NULL AS ACTUAL,
        ROUND(forecast) forecast,
        ROUND(lower_bound) lower_bound,
        ROUND(upper_bound) upper_bound
    FROM STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS
    WHERE MONTH_DATE BETWEEN DATEADD(year, -2, CURRENT_DATE()) AND DATEADD(month, 6, CURRENT_DATE())
),

FACT_FORECAST_CLOSED_SALES_RESULTS AS (

    SELECT
        REGION,
        MONTH_DATE,
        ACTUAL,
        forecast,
        lower_bound,
        upper_bound
    FROM V_CLOSED_SALES_MONTHLY

    UNION ALL

    SELECT
        REGION,
        MONTH_DATE,
        ACTUAL,
        forecast,
        lower_bound,
        upper_bound
    FROM FORECAST_CLOSED_SALES_RESULTS
    WHERE MONTH_DATE BETWEEN DATEADD(year, -2, CURRENT_DATE()) AND DATEADD(month, 6, CURRENT_DATE())
    ORDER BY REGION, MONTH_DATE
)

SELECT * FROM FACT_FORECAST_CLOSED_SALES_RESULTS