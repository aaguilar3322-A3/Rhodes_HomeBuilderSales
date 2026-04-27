-- This is your Cortex Project.
-----------------------------------------------------------
-- SETUP
-----------------------------------------------------------
use role ACCOUNTADMIN;
use warehouse ANALYTICS_WH;
use database RHODES;
use schema PROD_SALES;

-- Inspect the first 10 rows of your training data. This is the data we'll use to create your model.
select * from STAGING_SALES.V_REGIONAL_MANAGER_CLOSED_SALES limit 10;

-- Prepare your training data. Timestamp_ntz is a required format. Also, only include select columns.
CREATE OR REPLACE VIEW STAGING_SALES.V_CLOSED_SALES_MONTHLY AS 
SELECT REGION, DATE_FROM_PARTS(YEAR, MONTH, 1) MONTH_DATE, COUNT(ISCLOSED) TOTAL_CLOSED
FROM STAGING_SALES.V_REGIONAL_MANAGER_CLOSED_SALES
GROUP BY REGION, DATE_FROM_PARTS(YEAR, MONTH, 1)
ORDER BY DATE_FROM_PARTS(YEAR, MONTH, 1);



-----------------------------------------------------------
-- CREATE PREDICTIONS
-----------------------------------------------------------
-- Create your model.
CREATE OR REPLACE SNOWFLAKE.ML.FORECAST STAGING_SALES.forecast_closed_sales(
    INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'STAGING_SALES.V_CLOSED_SALES_MONTHLY'),
    SERIES_COLNAME => 'REGION',
    TIMESTAMP_COLNAME => 'MONTH_DATE',
    TARGET_COLNAME => 'TOTAL_CLOSED',
    CONFIG_OBJECT => { 'ON_ERROR': 'SKIP' }
);


-- Generate predictions and store the results to a table.
BEGIN
    -- This is the step that creates your predictions.
    CALL STAGING_SALES.forecast_closed_sales!FORECAST(
        FORECASTING_PERIODS => 30,
        -- Here we set your prediction interval.
        CONFIG_OBJECT => {'prediction_interval': 0.95}
    );
    LET x := SQLID;
    -- These steps store your predictions to a table.
    CREATE OR REPLACE TABLE STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS AS
    SELECT * FROM TABLE(RESULT_SCAN(:x));
END;



-- View your predictions.
SELECT * FROM STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS;

-- Union your predictions with your historical data, then view the results in a chart.
SELECT REGION, MONTH_DATE, ISCLOSED AS actual, NULL AS forecast, NULL AS lower_bound, NULL AS upper_bound
    FROM STAGING_SALES.V_CLOSED_SALES_MONTHLY
UNION ALL
SELECT replace(series, '"', '') as REGION, ts as MONTH_DATE, NULL AS actual, forecast, lower_bound, upper_bound
    FROM STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS;

-- Combine historical actuals with forecasted values
SELECT
    REGION,
    MONTH_DATE,
    TOTAL_CLOSED AS ACTUAL,
    NULL AS FORECAST,
    NULL AS LOWER_BOUND,
    NULL AS UPPER_BOUND
FROM STAGING_SALES.V_CLOSED_SALES_MONTHLY

UNION ALL

SELECT
    REPLACE(series, '"', '') AS REGION,
    ts AS MONTH_DATE,
    NULL AS ACTUAL,
    ROUND(forecast) forecast,
    ROUND(lower_bound) lower_bound,
    ROUND(upper_bound) upper_bound
FROM STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS
WHERE MONTH_DATE BETWEEN DATEADD(year, -2, CURRENT_DATE()) AND DATEADD(month, 6, CURRENT_DATE())
ORDER BY REGION, MONTH_DATE;

-- FINAL TABLE CREATED IN DBT USING QUERY BELOW IN PROD_SALES SCHEMA IN DBT
--fact_forecast_closed_sales_results.sql
--CREATES TABLE IN PROD_SALES}: fact_forecast_closed_sales_results
-----------------------------------------------------------
-- INSPECT RESULTS
-----------------------------------------------------------

-- Inspect the accuracy metrics of your model. 
CALL forecast_closed_sales!SHOW_EVALUATION_METRICS();

-- Inspect the relative importance of your features, including auto-generated features. 
CALL forecast_closed_sales!EXPLAIN_FEATURE_IMPORTANCE();
