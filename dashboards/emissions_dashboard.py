import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="ECCC Emissions Dashboard",
    page_icon="🌎",
    layout="wide",
)

st.title("ECCC Emissions Dashboard")
st.caption(
    "Business-facing visibility layer built on top of a tested dbt + DuckDB emissions mart."
)


# ---------------------------------------------------------
# Database connection
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DUCKDB_PATH = PROJECT_ROOT / "dev.duckdb"

MART_NAME = "mart_eccc_emissions_by_province_industry"


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DUCKDB_PATH.exists():
        st.error(f"DuckDB database not found at: {DUCKDB_PATH}")
        st.stop()

    query = f"""
        SELECT *
        FROM {MART_NAME}
    """

    with duckdb.connect(str(DUCKDB_PATH)) as con:
        return con.execute(query).df()


df = load_data()


# ---------------------------------------------------------
# Basic validation
# ---------------------------------------------------------

required_columns = {
    "reporting_year",
    "province",
    "industry_classification",
    "facility_count",
}

missing_columns = required_columns - set(df.columns)

if missing_columns:
    st.error(f"Missing expected columns: {', '.join(sorted(missing_columns))}")
    st.write("Available columns:", list(df.columns))
    st.stop()


# Try to detect emissions column
possible_emissions_columns = [
    "total_emissions_kt_co2e",
    "total_emissions_tonnes_co2e",
    "total_emissions",
    "emissions_tonnes_co2e",
    "emissions",
]

emissions_col = next(
    (col for col in possible_emissions_columns if col in df.columns),
    None,
)

if emissions_col is None:
    st.error(
        "Could not find an emissions column. "
        "Expected one of: "
        + ", ".join(possible_emissions_columns)
    )
    st.write("Available columns:", list(df.columns))
    st.stop()


# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------

st.sidebar.header("Filters")

years = sorted(df["reporting_year"].dropna().unique())
selected_years = st.sidebar.multiselect(
    "Reporting year",
    options=years,
    default=years,
)

provinces = sorted(df["province"].dropna().unique())
selected_provinces = st.sidebar.multiselect(
    "Province",
    options=provinces,
    default=provinces,
)

industries = sorted(df["industry_classification"].dropna().unique())
selected_industries = st.sidebar.multiselect(
    "Industry classification",
    options=industries,
    default=industries,
)

filtered_df = df[
    df["reporting_year"].isin(selected_years)
    & df["province"].isin(selected_provinces)
    & df["industry_classification"].isin(selected_industries)
].copy()


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

total_emissions = filtered_df[emissions_col].sum()
total_facilities = filtered_df["facility_count"].sum()
province_count = filtered_df["province"].nunique()
industry_count = filtered_df["industry_classification"].nunique()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total emissions", f"{total_emissions:,.0f}")
kpi2.metric("Facility count", f"{total_facilities:,.0f}")
kpi3.metric("Provinces", f"{province_count}")
kpi4.metric("Industries", f"{industry_count}")


st.divider()


# ---------------------------------------------------------
# Charts
# ---------------------------------------------------------

left, right = st.columns(2)

with left:
    st.subheader("Emissions by Province")

    emissions_by_province = (
        filtered_df.groupby("province", as_index=False)[emissions_col]
        .sum()
        .sort_values(emissions_col, ascending=False)
    )

    fig_province = px.bar(
        emissions_by_province,
        x="province",
        y=emissions_col,
        title="Total Emissions by Province",
        labels={
            "province": "Province",
            emissions_col: "Emissions",
        },
    )

    st.plotly_chart(fig_province, use_container_width=True)

with right:
    st.subheader("Emissions by Industry")

    emissions_by_industry = (
        filtered_df.groupby("industry_classification", as_index=False)[emissions_col]
        .sum()
        .sort_values(emissions_col, ascending=False)
        .head(15)
    )

    fig_industry = px.bar(
        emissions_by_industry,
        x=emissions_col,
        y="industry_classification",
        orientation="h",
        title="Top Industries by Emissions",
        labels={
            "industry_classification": "Industry",
            emissions_col: "Emissions",
        },
    )

    st.plotly_chart(fig_industry, use_container_width=True)


# ---------------------------------------------------------
# Year-over-year chart
# ---------------------------------------------------------

st.subheader("Emissions by Reporting Year")

emissions_by_year = (
    filtered_df.groupby("reporting_year", as_index=False)[emissions_col]
    .sum()
    .sort_values("reporting_year")
)

fig_year = px.line(
    emissions_by_year,
    x="reporting_year",
    y=emissions_col,
    markers=True,
    title="Total Emissions by Reporting Year",
    labels={
        "reporting_year": "Reporting Year",
        emissions_col: "Emissions",
    },
)

st.plotly_chart(fig_year, use_container_width=True)


# ---------------------------------------------------------
# Data table
# ---------------------------------------------------------

st.subheader("Province × Industry Summary")

summary_table = (
    filtered_df.groupby(
        ["reporting_year", "province", "industry_classification"],
        as_index=False,
    )
    .agg(
        total_emissions=(emissions_col, "sum"),
        facility_count=("facility_count", "sum"),
    )
    .sort_values(
        ["reporting_year", "total_emissions"],
        ascending=[False, False],
    )
)

st.dataframe(summary_table, use_container_width=True)


# ---------------------------------------------------------
# Methodology note
# ---------------------------------------------------------

with st.expander("About this dashboard"):
    st.write(
        """
        This dashboard is the business visibility layer for the dbt project.

        The underlying data comes from the dbt mart:

        `mart_eccc_emissions_by_province_industry`

        dbt is responsible for transformation, testing, documentation, and lineage.
        Streamlit is responsible for making the final modeled data explorable through
        filters, metrics, charts, and tables.
        """
    )