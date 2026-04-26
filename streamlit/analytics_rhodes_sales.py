import streamlit as st
import pandas as pd
import numpy as np
import snowflake.connector

import altair as alt

st.title("🏡 Rhodes Enterprises - Homebuilder Sales Performance")
st.write(
    "Insights for Regional Managers: sales trends, consultant performance, and regional activity."
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


# Query the fact_sales_by_region table
df_cs = pd.read_sql("SELECT * FROM fact_sales_by_region_my where year is not null", conn)

df_sr = pd.read_sql("SELECT * FROM fact_sales_by_region", conn)

df_agents = pd.read_sql("SELECT * FROM fact_sales_agent_closed_percent", conn)

# Query dimension regions table
df_c = pd.read_sql("SELECT distinct Region FROM dim_cities", conn)

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

# Modify color of sidebar filters
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #e6f2ff;
}
</style>
""", unsafe_allow_html=True)


# Create a sidebar with filters - include all filters from dimension tables    
with st.sidebar:
    st.header("Filters")

    regions = st.multiselect(
        "Region",
        df_c["REGION"].unique(),
        default=df_c["REGION"].unique()
    )

    managers = st.multiselect(
        "Regional Manager",
        df_rm["REGIONAL_MANAGER"].unique(),
        default=df_cs["REGIONAL_MANAGER"].unique()
    )

    #cities = st.multiselect(
    #    "City",
    #    df_c["CITY"].unique(),
    #    default=df_cs["CITY"].unique()
    #)

    #communities = st.multiselect(
    #    "Community",
    #    df_c["COMMUNITY"].unique(),
    #    default=df_cs["COMMUNITY"].unique()
    #)

    #consultants = st.multiselect(
    #    "Sales Consultant",
    #    df_sc["SALES_CONSULTANT"].unique(),
    #    default=df_cs["SALES_CONSULTANT"].unique()
    #)

    year = st.selectbox(
        "Year",
        sorted(df_my["YEAR"].unique())
    )

    #months = st.multiselect(
    #    "Month",
    #    df_my["MONTH"].unique(),
    #    default=df_cs["MONTH"].unique()
    #)

    #closedates = st.multiselect(
    #    "Close Date",
    #    df_cd["CLOSE_DATE"].unique(),
    #    default=df_cs["CLOSE_DATE"].unique()
    #)

# Apply filters globally to be able to interact with dashboard
filtered = df_cs[
    (df_cs["REGION"].isin(regions)) &
    (df_cs["REGIONAL_MANAGER"].isin(managers)) &
    #
    #(df_cs["CITY"].isin(cities)) &
    #(df_cs["COMMUNITY"].isin(communities)) &
    #(df_cs["SALES_CONSULTANT"].isin(consultants)) &
    (df_cs["YEAR"] == year)
     #&
    #(df_cs["MONTH"].isin(months)) &
    #(df_cs["CLOSE_DATE"].isin(closedates))
]

########## KPI for regional sales targets met (split by region) ##########

# KPI-specific filter: only region + regional manager
kpi_filtered_total_sales = df_sr[
    (df_sr["REGION"].isin(regions)) &
    (df_sr["REGIONAL_MANAGER"].isin(managers))
]

# Group by region
kpi_by_region = (
    kpi_filtered_total_sales
    .groupby("REGION", as_index=False)["SALES_TARGET_PCT"]
    .mean()
)

# Cap values at 100%
kpi_by_region["SALES_TARGET_PCT"] = kpi_by_region["SALES_TARGET_PCT"].clip(upper=100)

# Create KPI cards
cols = st.columns(len(kpi_by_region))

for idx, row in kpi_by_region.iterrows():
    region = row["REGION"]
    pct = row["SALES_TARGET_PCT"]

    # Color logic
    if pct >= 100:
        color = "#2ecc71"   # green
    elif pct >= 80:
        color = "#eed277"   # light yellow
    else:
        color = "#c52929"   # light red


    # Render KPI card
    cols[idx].markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:20px;
            font-weight:bold;
            ">
            {region}<br>
            <span style="font-size:28px;">{pct:.1f}%</span><br>
            <span style="font-size:14px;">Sales Target</span>
        </div>
        """,
        unsafe_allow_html=True
    )

########## Line chart for regional closed sales by month ##########
# Create a proper Month column for time-series plotting
filtered["MONTH_NAME"] = (
    filtered["MONTH"].astype(int)
    .astype(str)
    .str.zfill(2)
)

# Convert to month abbreviation (Jan, Feb, Mar…)
filtered["MONTH_NAME"] = pd.to_datetime(
    filtered["MONTH_NAME"], format="%m"
).dt.strftime("%b")

line_chart = (
    alt.Chart(filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "MONTH_NAME:N",
            title="Month",
            sort=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        ),
        y=alt.Y("sum(TOTAL_CLOSED):Q", title="Total Closed Sales"),
        color=alt.Color("REGION:N", title="Region"),
        tooltip=["REGION", "YEAR", "MONTH_NAME", "TOTAL_CLOSED"]
    )
    .properties(
        title=f"Total Closed Sales by Region ({year})",
        width="container"
    )
)



# Display line chart
st.altair_chart(line_chart, use_container_width=True)




########## Rank chart for sales consultants closed sales ##########
#left_col, right_col = st.columns([2, 1])
#with right_col:
rank_chart = (
    alt.Chart(df_agents)
    .mark_bar()
    .encode(
        y=alt.Y("SALES_CONSULTANT:N", sort="-x", title="Sales Consultant"),
        x=alt.X("TOTAL_CLOSED:Q", title="Total Homes Closed"),
        color=alt.Color(
            "CLOSING_RANK:O",
            scale=alt.Scale(
                domain=[1, 2, 3, 4, 5, 6],
                range=["#2ecc71", "#27ae60", "#f1c40f", "#e67e22", "#e65022", "#e74c3c"]
            ),
            title="Rank"
        ),
        tooltip=[
            "SALES_CONSULTANT",
            "CLOSING_RANK",
            "TOTAL_CLOSED",
            "TOTAL_UNDER_CONTRACT",
            "TOTAL_CANCELLED",
            "TOTAL_CONTRACTS",
            "CLOSEDPERCENT",
            "AVERAGE_COMMISSION"
        ]
    )
    .properties(
        title="🏆 Sales Consultant Performance Ranking",
        height=400
    )
)

st.altair_chart(rank_chart, use_container_width=True)



# Create charts using the metrics and dimensions
#chart = alt.Chart(filtered).mark_bar().encode(
#    x="CITY",
#    y="CONTRACT_PRICE",
#    color="CITY"
#)

#st.altair_chart(chart, use_container_width=True)

