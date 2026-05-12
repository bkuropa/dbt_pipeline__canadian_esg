select
    "Facility ID" as facility_id,
    "Facility name" as facility_name,
    "Company name" as company_name,
    City as city,
    Address as address,
    "Postal code" as postal_code,
    Province as province,
    Latitude as latitude,
    Longitude as longitude,
    "Total emissions" as total_emissions_kt_co2e,
    Unit as emissions_unit,
    Year as reporting_year,
    "Report year" as report_year,
    "Industry classification" as industry_classification,
    "Industry classification link" as industry_classification_link,
    "Facility information" as facility_information_url,
    "More information" as more_information_url
from {{ ref('eccc_large_facility_emissions_2024') }}