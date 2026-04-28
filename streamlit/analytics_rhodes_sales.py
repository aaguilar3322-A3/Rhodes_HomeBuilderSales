import streamlit as st
import pandas as pd
#import numpy as np
import snowflake.connector

import altair as alt

#from openai import OpenAI
#from snowflake.cortex import Complete


# Connect to Snowflake via secrets file (do not publish secrets file to git)
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
    #role=st.secrets["snowflake"]["role"]
)


# Query the fact_sales_by_region table
df_cs = pd.read_sql("SELECT * FROM fact_sales_by_region_my", conn)

df_sr = pd.read_sql("SELECT * FROM fact_sales_by_region", conn)

# Region KPI by year data
df_ry = pd.read_sql("select * from fact_sales_by_region_year", conn)

# Query sales agents fact tables
df_agents = pd.read_sql("SELECT MONTH_CLOSING_RANK, YEAR, MONTH, SALES_CONSULTANT, MONTH_AVERAGE_COMMISSION, MONTH_CLOSED, MONTH_UNDER_CONTRACT, MONTH_CANCELLED, MONTH_CONTRACTS, MONTH_CLOSED_PCT" \
" FROM fact_monthly_sales_agent_closed_percent", conn)

df_agents_yearly = pd.read_sql("SELECT * FROM fact_yearly_sales_agent_closed_percent", conn)

# Query dimension regions table
df_c = pd.read_sql("SELECT distinct Region FROM dim_cities", conn)

# Query sales_consultants table
df_sc = pd.read_sql("SELECT * FROM dim_sales_consultants", conn)

# Query regional managers table
df_rm = pd.read_sql("SELECT * FROM dim_regional_managers", conn)

# Query close dates table
df_cd = pd.read_sql("SELECT * FROM dim_close_dates", conn)

# Query close dates years and months table
df_my = pd.read_sql("SELECT distinct year, month FROM fact_sales_by_region_my", conn)

# Create filters
#regions = df["REGION"].unique()
#selected_region = st.selectbox("Select Region", regions)

#filtered = df[df["REGION"] == selected_region]

# Modify color of sidebar filters
st.markdown("""
<style>

/* Selected value chips inside multiselect */
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #cce6ff !important;   /* Light blue */
    color: #003366 !important;              /* Dark text */
    border-radius: 6px !important;
    border: 1px solid #99c2ff !important;
}

[data-testid="stSidebar"] {
    background-color: #e6f2ff;
}
            
[data-testid="stSidebar"] label {
    color: #003366 !important;   /* Navy blue labels */
    font-weight: 600 !important;
}
</st
            
/* Remove the default red hover */
[data-testid="stSidebar"] [data-baseweb="tag"]:hover {
    background-color: #b3d9ff !important;
    color: #003366 !important;
}

</style>
""", unsafe_allow_html=True)


# Create a sidebar with filters - include all filters from dimension tables    
with st.sidebar:
    st.header("Filters")
    
    year = st.selectbox(
        "Year",
        sorted(df_my["YEAR"].unique())
    )

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


    #months = st.multiselect(
    #    "Month",
    #    df_my["MONTH"].unique(),
    #    default=df_my["MONTH"].unique()
    #)

    #closedates = st.multiselect(
    #    "Close Date",
    #    df_cd["CLOSE_DATE"].unique(),
    #    default=df_cs["CLOSE_DATE"].unique()
    #)

# Apply filters globally to be able to interact with dashboard
filtered = df_cs[
    ((df_cs["YEAR"] == year) &
     df_cs["REGION"].isin(regions)) &
    (df_cs["REGIONAL_MANAGER"].isin(managers))


    #
    #(df_cs["CITY"].isin(cities)) &
    #(df_cs["COMMUNITY"].isin(communities)) &
    #(df_cs["SALES_CONSULTANT"].isin(consultants)) &
    
    #&
    #df_cs["MONTH"].isin(months) 
    #&
    #(df_cs["CLOSE_DATE"].isin(closedates))
]

########## Beginning of dashboard ##########
st.title("🏡 Rhodes Enterprises - Homebuilder Sales Performance")
st.write(
    "Insights for Regional Managers: sales trends, sales consultant performance, and projected sales."
)

########## KPI for regional sales targets met (split by region) ##########
st.subheader(f"🎯 Sales Target Achieved by Region in {year}")

# KPI-specific filter: only region + regional manager
kpi_filtered_total_sales = df_ry[
    (df_ry["YEAR"] == year) &
    (df_ry["REGION"].isin(regions)) &
    (df_ry["REGIONAL_MANAGER"].isin(managers))
]


# Consultant filter
df_agents_filtered = df_agents[
    (df_agents["YEAR"] == year) 
    #& (df_agents["MONTH"].isin(months))
]

# Group by region
kpi_by_region = (
    kpi_filtered_total_sales
    .groupby("REGION", as_index=False)
    .agg({
        "SALES_TARGET_PCT": "mean",
        "RM_SALES_TARGET_UNITS": "sum"   # or "mean" depending on your logic
    })
)

# Cap values at 100%
kpi_by_region["SALES_TARGET_PCT"] = kpi_by_region["SALES_TARGET_PCT"].clip(upper=100)

# Create KPI cards
cols = st.columns(len(kpi_by_region))

for idx, row in kpi_by_region.iterrows():
    region = row["REGION"]
    pct = row["SALES_TARGET_PCT"]
    target_units = row["RM_SALES_TARGET_UNITS"]

    # Color logic
    if pct >= 90:
        color = "#2ecc71"   # green
    elif pct >= 70:
        color = "#e2c76d"   # light yellow
    else:
        color = "#f14747"   # light red

    cols[idx].markdown(
        f"""
        <div style="
            background-color:{color};
            padding:15px;
            border-radius:10px;
            border:3px solid black;
            text-align:center;
            font-size:20px;
            font-weight:bold;
        ">
            {region}<br>
            <span style="font-size:22px;">{pct:.1f}%</span><br>
            <span style="font-size:16px; font-weight:600;">
                Sales Target: {target_units}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# Add spacing in between charts
st.write("")


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
        y=alt.Y("sum(TOTAL_CLOSED):Q", title="Sales Closed"),
        color=alt.Color("REGION:N", title="Region"),
        tooltip=["REGION", "YEAR", "MONTH_NAME", "TOTAL_CLOSED"]
    )
    .properties(
        title=f"📍 Total Closed Sales by Region ({year})",
        width="container"
    )
)

# Display line chart
st.altair_chart(line_chart, use_container_width=True)

# Add divider in between chart sections
st.write("")
st.divider()

########## Integrate Forecasting Model from Snowflake - Create Chart ##########
query = """select * from fact_forecast_closed_sales_results;"""

# Prepare charting data from forecast
df_forecast = pd.read_sql(query, conn)

df_long = df_forecast.melt(
    id_vars=["REGION", "MONTH_DATE"],
    value_vars=["ACTUAL", "FORECAST"],
    var_name="TYPE",
    value_name="VALUE"
)

df_long["REGION_ACTUAL"] = df_long["REGION"].where(df_long["TYPE"] == "ACTUAL")
df_long["REGION_FORECAST"] = df_long["REGION"].where(df_long["TYPE"] == "FORECAST")
df_long["REGION_ACTUAL"] = df_long["REGION_ACTUAL"].fillna("").apply(
    lambda x: f"{x} Actual" if x != "" else None
)

df_long["REGION_FORECAST"] = df_long["REGION_FORECAST"].fillna("").apply(
    lambda x: f"{x} Forecast" if x != "" else None
)

df_actual = df_long[df_long["TYPE"] == "ACTUAL"]
df_forecast = df_long[df_long["TYPE"] == "FORECAST"]


# Display and create forecasting chart
actual_chart = (
    alt.Chart(df_actual)
    .mark_line(point=True)
    .encode(
        x=alt.X("MONTH_DATE:T", title="Month / Year"),
        y=alt.Y("VALUE:Q", title="Sales Closed"),
        color=alt.Color(
            "REGION_ACTUAL:N",
            title="Region / Value"
        ),
        tooltip=["REGION", "MONTH_DATE", "VALUE"]
    )
)

forecast_chart = (
    alt.Chart(df_forecast)
    .mark_line(point=True)
    .encode(
        x=alt.X("MONTH_DATE:T", title="Month / Year"),
        y=alt.Y("VALUE:Q", title="Sales Closed"),
        color=alt.Color(
            "REGION_FORECAST:N",
            title="Region / Value"
        ),
        strokeDash=alt.value([4,4]),
        tooltip=["REGION", "MONTH_DATE", "VALUE"]
    )
)

forecast_start = df_actual["MONTH_DATE"].max()

separator = (
    alt.Chart(pd.DataFrame({"x": [forecast_start]}))
    .mark_rule(strokeDash=[4,4], color="gray")
    .encode(x="x:T")
)

forecast_labels = (
    alt.Chart(df_forecast)
    .mark_text(align="left", dx=5, dy=-5, fontSize=12)
    .encode(
        x="MONTH_DATE:T",
        y="VALUE:Q",
        text="REGION:N",
        color=alt.Color("REGION_FORECAST:N")
    )
    .transform_filter(
        alt.datum.MONTH_DATE == df_forecast["MONTH_DATE"].max()
    )
)


final_chart = (actual_chart + forecast_chart).properties(
    title="🌦️ Projected Closed Sales by Region (6 Month Forecast)",
    width="container",
    height=400
)

st.altair_chart(final_chart, use_container_width=True)
st.divider()


########## Rank chart for sales consultants closed sales ##########
# Layout: main content left, rank chart right
#left_col, right_col = st.columns([2, 1])

df_agents_yearly["SALES_CONSULTANT"] = df_agents_yearly["SALES_CONSULTANT"].str.strip().str.upper()

# Filter by year only
df_agents["SALES_CONSULTANT"] = df_agents["SALES_CONSULTANT"].str.strip().str.upper()

df_agents_filtered = df_agents[df_agents["YEAR"] == year].copy()
df_yearly_filtered = df_agents_yearly[df_agents_yearly["YEAR"] == year].copy()

df_agents_filtered = df_agents_filtered.merge(
    df_yearly_filtered[["YEAR", "SALES_CONSULTANT", "TOTAL_CLOSING_RANK", "TOTAL_CLOSED"]],
    on=["YEAR", "SALES_CONSULTANT"],
    how="left"
)

# Create month labels
df_agents_filtered["MONTH_NAME"] = (
    df_agents_filtered["MONTH"]
    .astype(int)
    .astype(str)
    .str.zfill(2)
)


df_agents_filtered["MONTH_NAME"] = pd.to_datetime(
    df_agents_filtered["MONTH_NAME"], format="%m"
).dt.strftime("%b")

st.subheader(f"🏅 Top 3 Sales Consultants of {year}")

top3 = df_yearly_filtered.nsmallest(3, "TOTAL_CLOSING_RANK")

medal_colors = ["#FFD700", "#C0C0C0", "#9C7353"]  # Gold, Silver, Bronze
medal_emojis = ["🥇", "🥈", "🥉"]

cols = st.columns(3)
for i, row in enumerate(top3.itertuples()):
    bg_color = medal_colors[i]  # pick gold, silver, bronze
    medal = medal_emojis[i]

    cols[i].markdown(
        f"""
        <div style="
            background-color:{bg_color};
            padding:15px;
            border-radius:10px;
            border:3px solid black;
            text-align:center;
            font-size:20px;
            font-weight:bold;
            color:black;
        ">
            {medal} {row.SALES_CONSULTANT}<br>
            <span style="font-size:16px;">Total Closed: {row.TOTAL_CLOSED}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Add spacing in between charts
st.write("")


#Sales Consultants -  Build line + scatter chart
consultant_trend_chart = (
    alt.Chart(df_agents_filtered)
    .mark_line(point=True)
    .encode(
        x=alt.X(
            "MONTH_NAME:N",
            title="Month",
            sort=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        ),
        y=alt.Y(
            "MONTH_CLOSED:Q",
            title="Sales Closed"
        ),
        color=alt.Color(
            "SALES_CONSULTANT:N",
            title="Sales Consultant"
        ),
        tooltip=[
            "SALES_CONSULTANT",
            "YEAR",
            "MONTH",
            "MONTH_CLOSED",
            "MONTH_CLOSED_PCT",
            "MONTH_CLOSING_RANK",
            "TOTAL_CLOSING_RANK",   # ⭐ YEARLY RANK ADDED HERE
            "MONTH_CONTRACTS",
            "MONTH_AVERAGE_COMMISSION"
        ]
    )
    .properties(
        title=f"📈 Sales Consultant Monthly Performance ({year})",
        height=450
    )
)

st.altair_chart(consultant_trend_chart, use_container_width=True)

# Add divider in between chart sections
st.divider()


 ########## Integrate Snowflake Cortex Complete chatbox with acces to my data schema ##########
st.header("💬 Ask Your Data (Snowflake Cortex)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Build context layer
def get_schema_context():
    query = """
    SELECT table_name, column_name
    FROM information_schema.columns
    WHERE table_schema IN ('PROD_SALES', 'STAGING_SALES')
    ORDER BY table_name, ordinal_position
    """
    df = pd.read_sql(query, conn)

    schema_text = ""
    for table, group in df.groupby("TABLE_NAME"):
        cols = ", ".join(group["COLUMN_NAME"])
        schema_text += f"{table}({cols})\n"

    return schema_text


def get_dashboard_context():
    return f"""
    DASHBOARD CONTEXT:

    KPI:
    - Sales Target % by Region (capped at 100%)
    - Color logic: Green >= 90%, Yellow >= 70%, Red < 70%

    CHARTS:
    1. Closed Sales by Region (Line Chart)
       Columns: REGION, MONTH, TOTAL_CLOSED

    2. Consultant Monthly Performance
       Columns: SALES_CONSULTANT, MONTH_CLOSED, MONTH_CLOSING_RANK

    3. Forecast Chart (Actual vs Forecast)
       Columns: REGION, MONTH_DATE, ACTUAL, FORECAST

    FILTERS:
    - Year
    - Region
    - Regional Manager

    TOP 3 CONSULTANTS:
    - Based on TOTAL_CLOSING_RANK (lower = better)
    """


# Data extraction for dashboard
def get_dashboard_metrics():
    return {
        "top3_consultants": top3.to_dict(orient="records"),
        "kpi_by_region": kpi_by_region.to_dict(orient="records"),
        "consultant_monthly": df_agents_filtered.to_dict(orient="records"),
        "regional_sales": filtered.to_dict(orient="records"),
        "forecast": df_forecast.to_dict(orient="records")
    }


def fetch_metric_from_ai_request(request):
    metrics = get_dashboard_metrics()
    request = request.lower()

    if "top 3" in request or "top three" in request:
        return metrics["top3_consultants"]

    if "kpi" in request or "target" in request:
        return metrics["kpi_by_region"]

    if "forecast" in request:
        return metrics["forecast"]

    if "consultant" in request:
        return metrics["consultant_monthly"]

    if "regional" in request or "region" in request:
        return metrics["regional_sales"]

    return None


# Call AI Model
MODEL_NAME = "mistral-large"   # Updated model


def ask_ai(prompt):
    schema = get_schema_context()
    dashboard = get_dashboard_context()

    query = f"""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        '{MODEL_NAME}',
        $$
        You are an expert data analyst for a homebuilder sales organization.

        You have access to:
        - Full Snowflake schema
        - Dashboard KPIs
        - Chart data
        - Forecast data
        - Consultant performance data

        IMPORTANT:
        If the user asks for specific values (like "top 3 consultants", 
        "sales for West region", "forecast for March"):
        → Respond with: DATA_REQUEST: <description>

        Examples:
        - "DATA_REQUEST: top 3 consultants"
        - "DATA_REQUEST: regional kpi"
        - "DATA_REQUEST: forecast"
        - "DATA_REQUEST: consultant monthly performance"

        If the user asks a business question:
        → Answer normally using dashboard logic.

        If the user asks for SQL:
        → Generate ONLY a SELECT query.

        SCHEMA:
        {schema}

        DASHBOARD:
        {dashboard}

        USER QUESTION:
        {prompt}
        $$
    )::STRING;
    """

    cur = conn.cursor()
    cur.execute(query)
    response = cur.fetchone()[0]
    cur.close()
    return response


# User input handling
user_input = st.chat_input("Ask a question about your sales data...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your data..."):
            response = ask_ai(user_input)

            # ⭐ Normalize AI response so detection ALWAYS works
            clean_response = (
                response.strip()
                .replace('"', "")
                .replace("'", "")
                .lower()
            )

            # ⭐ Detect DATA_REQUEST reliably
            if clean_response.startswith("data_request:"):
                req = clean_response.replace("data_request:", "").strip()
                data = fetch_metric_from_ai_request(req)

                if data is not None:
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)

                    final_response = f"Here are the values for: **{req}**"
                else:
                    final_response = "I couldn't match that request to a dataset."

                st.markdown(final_response)
                st.session_state.messages.append({"role": "assistant", "content": final_response})

            else:
                # Normal AI response
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
