import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector

import altair as alt

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Connect to Snowflake via secrets file (do not publish secrets file to git)
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"],
    #role=st.secrets["snowflake"]["role"]
)


# Query the fact table
df_cs = pd.read_sql("SELECT * FROM fact_closed_sales", conn)

# Query dimension cities table
df_c = pd.read_sql("SELECT * FROM dim_cities", conn)

# Query sales_consultants table
df_sc = pd.read_sql("SELECT * FROM dim_sales_consultants", conn)

# Query regional managers table
df_rm = pd.read_sql("SELECT * FROM dim_regional_managers", conn)

# Query close dates table
df_cd = pd.read_sql("SELECT * FROM dim_close_dates", conn)

# Query close dates years and months table
df_my = pd.read_sql("SELECT * FROM dim_close_date_my", conn)

# Create filters
#regions = df["REGION"].unique()
#selected_region = st.selectbox("Select Region", regions)

#filtered = df[df["REGION"] == selected_region]

# Create a sidebar with filters - include all filters from dimension tables    
with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        df_c["REGION"].unique(),
        default=df_cs["REGION"].unique()
    )

    managers = st.multiselect(
        "Regional Manager",
        df_rm["REGIONAL_MANAGER"].unique(),
        default=df_cs["REGIONAL_MANAGER"].unique()
    )

    cities = st.multiselect(
        "City",
        df_c["CITY"].unique(),
        default=df_cs["CITY"].unique()
    )

    communities = st.multiselect(
        "Community",
        df_c["COMMUNITY"].unique(),
        default=df_cs["COMMUNITY"].unique()
    )

    consultants = st.multiselect(
        "Sales Consultant",
        df_sc["SALES_CONSULTANT"].unique(),
        default=df_cs["SALES_CONSULTANT"].unique()
    )

    years = st.multiselect(
        "Year",
        df_my["YEAR"].unique(),
        default=df_cs["YEAR"].unique()
    )

    months = st.multiselect(
        "Month",
        df_my["MONTH"].unique(),
        default=df_cs["MONTH"].unique()
    )

    closedates = st.multiselect(
        "Close Date",
        df_cd["CLOSE_DATE"].unique(),
        default=df_cs["CLOSE_DATE"].unique()
    )


# Apply filters globally to be able to interact with dashboard
filtered = df_cs[
    (df_cs["REGION"].isin(regions)) &
    (df_cs["REGIONAL_MANAGER"].isin(managers)) &
    (df_cs["CITY"].isin(cities)) &
    (df_cs["COMMUNITY"].isin(communities)) &
    (df_cs["SALES_CONSULTANT"].isin(consultants)) &
    (df_cs["YEAR"].isin(years)) &
    (df_cs["MONTH"].isin(months)) &
    (df_cs["CLOSE_DATE"].isin(closedates))
]

# Create charts using the metrics and dimensions
chart = alt.Chart(filtered).mark_bar().encode(
    x="CITY",
    y="CONTRACT_PRICE",
    color="CITY"
)

st.altair_chart(chart, use_container_width=True)