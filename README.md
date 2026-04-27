Rhodes Enterprises – Modern Homebuilder Sales Analytics Platform
An end-to-end data pipeline transforming raw homebuilder sales data, for Rhodes, into a model that is analysis-ready and integrated AI-enhanced dashboard. Pipeline is built with Snowflake, dbt, Streamlit, and Snowflake Cortex (AI).

Overview
This project delivers an end‑to‑end sales analytics platform designed for homebuilder operations.

It integrates:
- Snowflake ingestion pipelines for loading raw sales, consultant, and regional data
- dbt models for transforming raw data into clean, analytics‑ready marts
- A Streamlit dashboard for interactive insights, KPIs, and forecasting
- AI-powered features (Cortex/Snowflake functions) for natural‑language insights and automated analysis

The goal: provide Regional Managers and Sales Leadership with real‑time visibility into performance, targets, and forecasting.

Components
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

 Folder Structure
 -  Snowflake
   - /snowflake
 - dbt
   - Models
     - Staging: Clean and stage raw data
       - /models/staging/sales
     - Intermeidate: Table joins and business logiv
       - /models/intermediate/sales
     - Marts: Fact & dimension tables for reporting
       - /models/marts/sales
         
Features
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
