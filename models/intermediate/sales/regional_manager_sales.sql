{{ config(materialized='table') }}

WITH 
region_managers AS (
    SELECT * FROM {{ ref('stg_regional_managers') }}
),
hb_sales AS (
    SELECT * FROM {{ ref('stg_homebuilder_sales') }}
),
regional_manager_sales AS(
SELECT
    date_part('month', s.CLOSE_DATE) AS Month,
    date_part('year', s.CLOSE_DATE) AS Year,
	s.CONTRACT_ID,
	s.COMMUNITY,
	s.CITY,
	s.REGION,
	r.REGIONAL_MANAGER,
	r.SALES_TARGET_UNITS AS RM_SALES_TARGET_UNITS,
	r.MARGIN_TARGET_PCT AS RM_MARGIN_TARGET_PCT,
	s.PLAN_NAME,
	s.SQFT,
	s.BEDROOMS,
	s.BATHROOMS,
	s.BASE_PRICE,
	s.UPGRADE_AMOUNT,
	s.INCENTIVE_AMOUNT,
	s.CONTRACT_PRICE,
	s.CONTRACT_DATE,
	s.CLOSE_DATE,
    s.DAYS_TO_CLOSE,
	s.STATUS,
	s.BUYER_SOURCE,
	s.AGENT_COMMISSION,
	s.LOAN_TYPE,
	s.SALES_CONSULTANT,
    (s.CONTRACT_PRICE / s.SQFT) AS PRICE_PER_SQFT,
    (s.UPGRADE_AMOUNT + s.INCENTIVE_AMOUNT) AS TOTAL_INCENTIVES,
    (s.INCENTIVE_AMOUNT + s.UPGRADE_AMOUNT + s.CONTRACT_PRICE) AS TOTAL_SALES_PRICE,
    IFNULL(DATEDIFF('day', s.CONTRACT_DATE, s.CLOSE_DATE),0) AS TOTAL_DAYS_TO_CLOSE,
    CASE WHEN UPPER(s.status) = 'CANCELLED' THEN 1 ELSE 0 END CANCELLED_FLAG
FROM hb_sales AS s
LEFT JOIN region_managers AS r ON s.REGION = r.REGION
)

SELECT * FROM regional_manager_sales