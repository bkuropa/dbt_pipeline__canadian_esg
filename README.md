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
