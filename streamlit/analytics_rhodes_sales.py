import streamlit as st
import pandas as pd
import snowflake.connector

import altair as alt

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"],
    #role=st.secrets["snowflake"]["role"]
)


# Query your fact table
df_avg_c_sp = pd.read_sql("SELECT * FROM FACT_AVG_CITY_SALES_PRICE", conn)

df_c = pd.read_sql("SELECT * FROM dim_cities", conn)

df_rm = pd.read_sql("SELECT * FROM dim_regional_managers", conn)

# Create filters
#regions = df["REGION"].unique()
#selected_region = st.selectbox("Select Region", regions)

#filtered = df[df["REGION"] == selected_region]
    
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

# Apply filters to all
filtered = df_avg_c_sp[
    (df_c["REGION"].isin(regions)) &
    (df_rm["REGIONAL_MANAGER"].isin(managers)) &
    (df_c["CITY"].isin(cities)) &
    (df_c["COMMUNITY"].isin(communities)) 
    #&
    #(df["SALES_CONSULTANT"].isin(consultants))
]


chart = alt.Chart(filtered).mark_bar().encode(
    x="CITY",
    y="AVG_SALESPRICE_PER_CITY",
    color="CITY"
)

st.altair_chart(chart, use_container_width=True)

#st.bar_chart(filtered["DAYS_TO_CLOSE"])
#cancel_rate = (
#    filtered.groupby("REGIONAL_MANAGER")["CANCELLED_FLAG"]
#    .mean()
#    .reset_index()
#)

#st.bar_chart(cancel_rate, x="REGIONAL_MANAGER", y="CANCELLED_FLAG")

#
