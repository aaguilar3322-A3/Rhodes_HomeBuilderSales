**Rhodes Enterprises – Homebuilder Sales Analytics Platform**

**Overview:**
- This project delivers an end‑to‑end sales analytics platform designed for homebuilder operations.
- End-to-end data pipeline transforming raw homebuilder sales data, into a model that is analysis-ready and integrated AI-enhanced dashboard.
- Pipeline is built with Snowflake, dbt, Streamlit, and Snowflake Cortex (AI).


**Streamlit App:**
-  URL: [Rhodes Enterprises - Homebuilder Sales Performance](https://analytics-rhodes-sales-x16323452.streamlit.app/)

**Integration:**
- Snowflake ingestion pipelines for loading raw sales, consultant, and regional data
- dbt models for transforming raw data into clean, analytics‑ready marts
- A Streamlit dashboard for interactive insights, KPIs, and forecasting
- AI-powered features (Cortex/Snowflake functions) for natural‑language insights and automated analysis

**Goal:**
- Provide Regional Managers and Sales Leadership with real‑time visibility into performance, targets, and forecasting.

**Components:**
- Snowflake
  - Raw file storage
  - Ingestion SQL scripts
  - Warehouse, database, & schema setup
  - Secrets management
- dbt
  - Staging models
  - Intermediate transformations
  - Sales marts (fact & dimension tables)
  - Tests & documentation
- Streamlit
  - KPI dashboards
  - Regional performance views
  - Sales consultant rankings
  - Forecasting visualizations
- AI Integration
  - Natural‑language Q&A
  - Automated summaries
  - Insight generation
- Github
  - Version Control
  - Repo / Documentation

**Folder Structure:**
-  Snowflake
    - /snowflake
 - dbt
   - Models
     - Staging: Clean and stage raw data
       - /models/staging/sales
       - <img width="186" height="87" alt="image" src="https://github.com/user-attachments/assets/db6331ec-4326-45d0-a9ab-e5f86419ef68" />

     - Intermeidate: Table joins and business logiv
       - /models/intermediate/sales
       - <img width="273" height="87" alt="image" src="https://github.com/user-attachments/assets/8ec435d0-3eb7-40ee-a3be-7762574e5bd3" />
     - Marts: Fact & dimension tables for reporting
       - /models/marts/sales
       - <img width="264" height="444" alt="image" src="https://github.com/user-attachments/assets/2160aa55-7bf2-4f37-84dd-b685f301c6af" />

**Snowflake Schema Structure:**
-  Data Warehouse
  - ANALYTICS_WH 
-  Database
  - RHODES   
-  Schema
   - PROD_SALES
     - PROD_SALES.DIM_CITIES
     - PROD_SALES.DIM_CLOSE_DATES
     - PROD_SALES.DIM_CLOSE_DATE_MY
     - PROD_SALES.DIM_REGIONAL_MANAGERS
     - PROD_SALES.DIM_SALES_CONSULTANTS
     - PROD_SALES.FACT_AVERAGE_SALES_COMISSION
     - PROD_SALES.FACT_AVG_CITY_SALES_PRICE
     - PROD_SALES.FACT_AVG_REGION_SALES_PRICE
     - PROD_SALES.FACT_AVG_SALES_DAYS_TO_CLOSE
     - PROD_SALES.FACT_BUYERS_SOURCE_PERCENT
     - PROD_SALES.FACT_CLOSED_SALES
     - PROD_SALES.FACT_FORECAST_CLOSED_SALES_RESULTS
     - PROD_SALES.FACT_MONTHLY_SALES_AGENT_CLOSED_PERCENT
     - PROD_SALES.FACT_REGION_SALES_PRICE
     - PROD_SALES.FACT_SALES_AGENT_CLOSED_PERCENT
     - PROD_SALES.FACT_SALES_BY_REGION
     - PROD_SALES.FACT_SALES_BY_REGION_MY
     - PROD_SALES.FACT_SALES_BY_REGION_YEAR
     - PROD_SALES.FACT_SALES_PRICE_PER_SQFT
     - PROD_SALES.FACT_YEARLY_SALES_AGENT_CLOSED_PERCENT 
   - STAGING_SALES
     - TABLES: 
       - STAGING_SALES.FORECAST_CLOSED_SALES
       - STAGING_SALES.FORECAST_CLOSED_SALES_RESULTS
       - STAGING_SALES.HOMEBUILDER_SALES_RAW
       - STAGING_SALES.REGIONAL_MANAGERS_RAW
       - STAGING_SALES.REGIONAL_MANAGER_CLOSED_SALES
       - STAGING_SALES.REGIONAL_MANAGER_SALES
       - STAGING_SALES.STG_HOMEBUILDER_SALES
       - STAGING_SALES.STG_REGIONAL_MANAGERS
     - VIEWS:
       - STAGING_SALES.V_CLOSED_SALES_MONTHLY
       - STAGING_SALES.V_REGIONAL_MANAGER_CLOSED_SALES
       - STAGING_SALES.V_REGIONAL_MANAGER_SALES
         
**Features:**
1. Automated Snowflake Ingestion
   - Loads sales, consultant, and regional data
   - Cleans and normalizes source files
   - Supports incremental ingestion
2. dbt Transformations
   - Staging → intermediate → marts
   - Fact tables for:
     - Monthly sales
     - Yearly consultant performance
     - Regional targets
   - Dimension tables for:
     - Consultants
     - Managers
     - Communities
   - Built‑in tests (unique, not null, relationships)
3. Streamlit Dashboard
   - Sidebar filters (Year, Region, Manager)
   - KPI cards with medal‑tier styling
   - Regional sales target performance
   - Consultant rankings (Top 3)
   - Monthly performance trend lines
   - Forecasting charts (Actual vs Forecast)
4. AI Integration
   - Natural‑language insights
   - Automated summaries
   - Cortex powered analysis
