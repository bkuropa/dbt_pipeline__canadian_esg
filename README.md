## Project Purpose

This project demonstrates a local ESG analytics engineering workflow using dbt and DuckDB.

The pipeline ingests Canadian ECCC emissions data, transforms it through documented dbt models, applies data quality tests, and produces a final mart for province- and industry-level emissions analysis.

The goal is to show the full analytics path:

```text
raw ECCC data
   ↓
dbt staging models
   ↓
tested/documented mart model
   ↓
dbt docs lineage
   ↓
business-facing dashboard layer
```

## Key dbt Commands

Run the ECCC-tagged models:

dbt run --select tag:eccc

Run ESG-related tests:

dbt test --select tag:esg

Build the final emissions mart:

dbt build --select mart_eccc_emissions_by_province_industry

Generate dbt documentation:

dbt docs generate

Serve dbt documentation locally:

dbt docs serve
Documentation and Lineage

dbt docs provides the engineering visibility layer for this project.

# It shows:

model lineage
YAML documentation
column descriptions
model dependencies
tests attached to models and columns
how the final mart is produced from upstream transformations

This is useful for understanding the structure, governance, and quality controls behind the pipeline.

# Business Visibility Layer

dbt docs explains how the data pipeline works, but it does not provide the final business-facing layer where users can explore real data through tables, charts, filters, and summary metrics.

The next planned layer is a lightweight dashboard that consumes the final DuckDB mart and displays the modeled emissions data visually.

## Planned dashboard features include:

KPI cards for total emissions, facility count, provinces, and industries
filters for reporting year, province, and industry classification
emissions by province
emissions by industry
province × industry summary table
optional year-over-year comparisons
explanatory notes connecting the dashboard back to the dbt mart and data tests

This layer is intended to mirror the final visibility step found in real ESG platforms: moving from governed data models into stakeholder-facing insight.

Planned Architecture
ECCC source data
   ↓
DuckDB local warehouse
   ↓
dbt staging models
   ↓
dbt mart model
   ↓
dbt tests and documentation
   ↓
Streamlit dashboard
   ↓
business-facing ESG insights
Final Mart

The core analytical output is:

mart_eccc_emissions_by_province_industry

This model is designed to support province- and industry-level emissions analysis using tested and documented transformation logic.
