select
    reporting_year,
    company_name,

    count(distinct facility_id) as facility_count,
    count(distinct province) as province_count,
    sum(total_emissions_kt_co2e) as total_emissions_kt_co2e,
    avg(total_emissions_kt_co2e) as avg_facility_emissions_kt_co2e,
    max(total_emissions_kt_co2e) as max_facility_emissions_kt_co2e,

    rank() over (
        partition by reporting_year
        order by sum(total_emissions_kt_co2e) desc
    ) as company_emissions_rank

from {{ ref('int_eccc_facility_emissions_quality') }}

group by
    reporting_year,
    company_name