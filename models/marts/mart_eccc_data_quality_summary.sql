select
    reporting_year,

    count(*) as total_facility_records,

    sum(case when has_missing_facility_id then 1 else 0 end) as missing_facility_id_count,
    sum(case when has_missing_facility_name then 1 else 0 end) as missing_facility_name_count,
    sum(case when has_missing_company_name then 1 else 0 end) as missing_company_name_count,
    sum(case when has_missing_province then 1 else 0 end) as missing_province_count,
    sum(case when has_missing_emissions then 1 else 0 end) as missing_emissions_count,
    sum(case when has_negative_emissions then 1 else 0 end) as negative_emissions_count,
    sum(case when has_zero_coordinates then 1 else 0 end) as zero_coordinate_count,
    sum(case when has_missing_city then 1 else 0 end) as missing_city_count,
    sum(case when has_missing_address then 1 else 0 end) as missing_address_count,
    sum(case when has_missing_or_placeholder_postal_code then 1 else 0 end) as missing_or_placeholder_postal_code_count

from {{ ref('int_eccc_facility_emissions_quality') }}

group by
    reporting_year