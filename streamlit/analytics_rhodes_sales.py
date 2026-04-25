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
    warehouse="ANALYTICS_WH",
    database="RHODES",
    schema="STAGING_SALES"
)

# Query your fact table
df = pd.read_sql("FACT_AVG_CITY_SALES_PRICE", conn)

regions = df["REGION"].unique()
selected_region = st.selectbox("Select Region", regions)

filtered = df[df["REGION"] == selected_region]



chart = alt.Chart(filtered).mark_bar().encode(
    x="CITY",
    y="mean(PRICE_PER_SQFT)",
    color="REGION"
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
