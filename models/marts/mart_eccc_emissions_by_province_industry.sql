select
    reporting_year,
    report_year,
    province,
    industry_classification,

    count(*) as facility_count,
    sum(total_emissions_kt_co2e) as total_emissions_kt_co2e,
    avg(total_emissions_kt_co2e) as avg_facility_emissions_kt_co2e,
    max(total_emissions_kt_co2e) as max_facility_emissions_kt_co2e,

    sum(case when has_zero_coordinates then 1 else 0 end) as zero_coordinate_count,
    sum(case when has_missing_city then 1 else 0 end) as missing_city_count,
    sum(case when has_missing_address then 1 else 0 end) as missing_address_count,
    sum(case when has_missing_or_placeholder_postal_code then 1 else 0 end) as missing_or_placeholder_postal_code_count

from {{ ref('int_eccc_facility_emissions_quality') }}

group by
    reporting_year,
    report_year,
    province,
    industry_classification