select
    reporting_year,
    facility_id,
    facility_name,
    company_name,
    province,
    city,
    industry_classification,
    total_emissions_kt_co2e,
    rank() over (
        partition by reporting_year
        order by total_emissions_kt_co2e desc
    ) as national_emissions_rank
from {{ ref('int_eccc_facility_emissions_quality') }}