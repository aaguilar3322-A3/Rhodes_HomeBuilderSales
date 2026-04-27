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
- Real‑time visibility into sales performance
- Consultant and regional KPIs
- Trend analysis and forecasting
- AI‑generated insights and summaries
- A single source of truth for sales reporting

**Architecture:**
- Snowflake
  - Raw file ingestion (CSV → Snowflake stage → tables)
  - STAGING_SALES schema for raw + lightly transformed data
  - PROD_SALES schema for dbt‑generated fact/dim tables
  - Warehouse + role/security setup
  - Cortex SQL functions for AI insights

- dbt
  - Staging → Intermediate → Marts model hierarchy
  - Fact & dimension modeling
  - Data quality tests (unique, not null, relationships)
  - Documentation & lineage graph
  - Production‑ready SQL transformations

- Streamlit
  - KPI dashboards
  - Regional performance views
  - Consultant rankings
  - Trend & forecasting visualizations
  - Natural‑language AI insights (Cortex via SQL)
- AI Integration
  - Snowflake Cortex SQL functions
  - Automated summaries
  - Natural‑language Q&A
  - Insight generation based on warehouse data
 
**Repo Structure:**
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
     - Lineage:
       - <img width="1173" height="1143" alt="image" src="https://github.com/user-attachments/assets/ab6c64df-c44e-4f44-88d5-e7021456f183" />
- Streamlit
  - /streamlit/analytics_rhodes_sales.py


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
     - Yearly sales
     - Yearly consultant performance
     - Regional targets
     - Closed sales by buyer;s Source
     - Average region sales prices
     - Average sales days to close
     - Forecasted Closed Sales
   - Dimension tables for:
     - Sales Consultants
     - Regional Managers
     - Communities
     - Month/Year Close Dates
   - Built‑in tests (unique, not null, relationships)
3. Streamlit Dashboard
   - Sidebar filters (Year, Region, Regional Manager)
   - KPI cards with medal‑tier styling
   - Regional sales target performance
   - Top 3 Sales Consultant rankings
   - Yearly Sales by Sales Consultants
   - Monthly performance trend lines
   - Forecasting charts (Actual vs Forecast)
4. AI Integration
   - Natural‑language insights
   - Automated summaries
   - Cortex powered analysis

**Setup Overview:**
- Create schemas for stage and prod
- Create stage for data files
  - <img width="1439" height="977" alt="image" src="https://github.com/user-attachments/assets/f2807043-ca57-4599-8a41-0ea6439f0026" />
- Load data files into stage
  -
- Load into tables
  - <img width="1272" height="575" alt="image" src="https://github.com/user-attachments/assets/8ae401f7-36ce-4326-8cf8-8d6faf0dab2e" />
  - <img width="759" height="762" alt="image" src="https://github.com/user-attachments/assets/a8c69b92-73a7-4576-ae3f-c39fb4080a02" />
  - <img width="1270" height="579" alt="image" src="https://github.com/user-attachments/assets/124bd5af-1e1c-4657-9906-ad6829b43151" />
- Create User Account
  - <img width="1245" height="642" alt="image" src="https://github.com/user-attachments/assets/78f09a88-6096-4795-84ad-8c3d265ade03" />
- Generate token for user
  - <img width="1990" height="840" alt="image" src="https://github.com/user-attachments/assets/915d1a0e-b5c3-4112-83d6-fd47d5ea18b4" />
  - <img width="562" height="588" alt="image" src="https://github.com/user-attachments/assets/3bc05322-dcec-44a8-bc62-ebf1f71e9dc5" />
- Create GitHub Repo
  - <img width="359" height="254" alt="image" src="https://github.com/user-attachments/assets/78e5e89a-87e1-404b-a57b-2a762fa4f460" />
  - <img width="772" height="790" alt="image" src="https://github.com/user-attachments/assets/eb8e5bed-fcf9-4840-9ea8-f0c854ae4936" />
  NOTE: Set repo to public
- Create dbt project
  - <img width="1753" height="610" alt="image" src="https://github.com/user-attachments/assets/a177badd-94b4-44bf-82cf-1a7918671f94" />
- Create Snowflake connection in dbt
  - [Connect To Snowflake In dbt Cloud](https://youtu.be/XH8ZGMmyG8A?si=5HhUIRbH6zSbrfnN)
  - <img width="832" height="379" alt="image" src="https://github.com/user-attachments/assets/7633b023-32af-407b-825b-ad68b39ba427" />
  - <img width="976" height="494" alt="image" src="https://github.com/user-attachments/assets/0c5e3189-ba73-454c-b047-4b9a93242f17" />
  - Snowflake: Copy URL and remove "https://" and ".snowflakecomputing.com" to leave account
  - <img width="1921" height="764" alt="image" src="https://github.com/user-attachments/assets/d9e29c5d-ecc6-4ea1-9867-d42f69568baf" />
  - <img width="812" height="821" alt="image" src="https://github.com/user-attachments/assets/a502dc4e-ea15-4cb5-8580-2768f71e8c9d" />
  - <img width="711" height="1302" alt="image" src="https://github.com/user-attachments/assets/cf1d697c-bcfd-453f-a1c8-ff6cb17ff951" />
- Link GitHub repo to dbt project
  - <img width="672" height="680" alt="image" src="https://github.com/user-attachments/assets/f1ccd26a-f074-40a6-a9dc-4391782fa2a6" />
  - <img width="534" height="854" alt="image" src="https://github.com/user-attachments/assets/8c61c6ef-233f-402c-8d3c-a06bb82ab7cd" />
  - <img width="319" height="292" alt="image" src="https://github.com/user-attachments/assets/c3adbcdd-4d77-4136-962e-e2902944016d" />
  - <img width="1005" height="885" alt="image" src="https://github.com/user-attachments/assets/30761b9b-dae2-417b-a2f9-1efd899475cc" />
- Create folder hierarchy in dbt project
  - <img width="257" height="172" alt="image" src="https://github.com/user-attachments/assets/6d52147b-14fa-4dd5-90e0-b172586be64b" />
- Create streamlit folder in repo
  - <img width="283" height="106" alt="image" src="https://github.com/user-attachments/assets/d3d7510c-5bda-4349-b93f-2bade6a6fafb" />
  - NOTE: Create a /.streamlit folder in inside /streamlit to include the secrets file used in streamlit connection to snowflake
- Create streamlit App and allow public access
  - <img width="1034" height="653" alt="image" src="https://github.com/user-attachments/assets/0d77bd74-13b0-4bb5-9371-0f3367563c38" />
  - <img width="559" height="777" alt="image" src="https://github.com/user-attachments/assets/1e807efa-8382-400f-a947-dac761005edf" />
  - <img width="905" height="538" alt="image" src="https://github.com/user-attachments/assets/909e2346-abaa-4163-ab71-3c6b18d44791" />
- Install dependent python libraries
- Update Streamlit app and Implement AI Chatbox & deploy
  - <img width="945" height="381" alt="image" src="https://github.com/user-attachments/assets/0fe1d369-3d3e-4e63-b72d-7dfae3b1401f" />
- Deploy Github repo

**Future Development & Features:**
- Further exploration of AI dashboard functionality
- Python connector in Snowflake
- Identity lookup dimension & intermediate tables
  - To better improve on star schema, create unique IDs or compoite keys on dimension and fact tables
  - Join by IDs rather than by string values
- Create a dev, stage, and prod environment
- Explore secret storing alternatives
- Schedule pipeline and run app
- Stream app additional charts/KPIs
  - Regional margin targets
  - Forecasting various metrics
  - Sales Matrix Table - region, city, community
  - Average City Sales Prices
  - Average Sales days to close
  - Average Regional Sales Prices
  - Average Sales Consultant Comission
  - Sales by Buyer's Source
  - Sales by Community
  - Sales by City
  - Filters: Date Range, Communities, Cities, Plan, Buyer's Source, Sales_Consultant
