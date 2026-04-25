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


<<<<<<< HEAD
# Create filters
#regions = df["REGION"].unique()
#selected_region = st.selectbox("Select Region", regions)

#filtered = df[df["REGION"] == selected_region]
    
with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        df["REGION"].unique(),
        default=df["REGION"].unique()
    )

    managers = st.multiselect(
        "Regional Manager",
        df["REGIONAL_MANAGER"].unique(),
        default=df["REGIONAL_MANAGER"].unique()
    )

    cities = st.multiselect(
        "City",
        df["CITY"].unique(),
        default=df["CITY"].unique()
    )

    communities = st.multiselect(
        "Community",
        df["COMMUNITY"].unique(),
        default=df["COMMUNITY"].unique()
    )

    #consultants = st.multiselect(
    #    "Sales Consultant",
    #    df["SALES_CONSULTANT"].unique(),
    #    default=df["SALES_CONSULTANT"].unique()
    #)

# Apply filters to all
filtered = df[
    (df["REGION"].isin(regions)) &
    (df["REGIONAL_MANAGER"].isin(managers)) &
    (df["CITY"].isin(cities)) &
    (df["COMMUNITY"].isin(communities)) &
#    (df["SALES_CONSULTANT"].isin(consultants))
]
=======
# Query the fact table
df_avg_c_sp = pd.read_sql("SELECT * FROM FACT_AVG_CITY_SALES_PRICE", conn)

# Query dimension cities table
df_c = pd.read_sql("SELECT * FROM dim_cities", conn)

# Query regional managers table
df_rm = pd.read_sql("SELECT * FROM dim_regional_managers", conn)
>>>>>>> 930195e2f7b9faa4da68a69c5fc0cb2ab38c7e68

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
        default=df_avg_c_sp["REGION"].unique()
    )

    managers = st.multiselect(
        "Regional Manager",
        df_rm["REGIONAL_MANAGER"].unique(),
        default=df_avg_c_sp["REGIONAL_MANAGER"].unique()
    )

    cities = st.multiselect(
        "City",
        df_c["CITY"].unique(),
        default=df_avg_c_sp["CITY"].unique()
    )

    communities = st.multiselect(
        "Community",
        df_c["COMMUNITY"].unique(),
        default=df_avg_c_sp["COMMUNITY"].unique()
    )

    #consultants = st.multiselect(
    #    "Sales Consultant",
    #    df["SALES_CONSULTANT"].unique(),
    #    default=df["SALES_CONSULTANT"].unique()
    #)

# Apply filters globally to be able to interact with dashboard
filtered = df_avg_c_sp[
    (df_c["REGION"].isin(regions)) &
    (df_rm["REGIONAL_MANAGER"].isin(managers)) &
    (df_c["CITY"].isin(cities)) &
    (df_c["COMMUNITY"].isin(communities)) 
    #&
    #(df["SALES_CONSULTANT"].isin(consultants))
]

# Create charts using the metrics and dimensions
chart = alt.Chart(filtered).mark_bar().encode(
    x="CITY",
<<<<<<< HEAD
    y="mean(FACT_AVG_CITY_SALES_PRICE)",
    color="REGION"
=======
    y="AVG_SALESPRICE_PER_CITY",
    color="CITY"
>>>>>>> 930195e2f7b9faa4da68a69c5fc0cb2ab38c7e68
)

st.altair_chart(chart, use_container_width=True)

#st.bar_chart(filtered["DAYS_TO_CLOSE"])
#cancel_rate = (
#    filtered.groupby("REGIONAL_MANAGER")["CANCELLED_FLAG"]
#    .mean()
#    .reset_index()
#)

#st.bar_chart(cancel_rate, x="REGIONAL_MANAGER", y="CANCELLED_FLAG")

# Create line chart using metrics and dimensions
chart_data = pd.DataFram(
    
)
