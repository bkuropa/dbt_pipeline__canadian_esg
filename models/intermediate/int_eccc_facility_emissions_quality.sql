select
    *,
    
    case
        when facility_id is null then true
        else false
    end as has_missing_facility_id,

    case
        when facility_name is null or trim(facility_name) = '' then true
        else false
    end as has_missing_facility_name,

    case
        when company_name is null or trim(company_name) = '' then true
        else false
    end as has_missing_company_name,

    case
        when province is null or trim(province) = '' then true
        else false
    end as has_missing_province,

    case
        when total_emissions_kt_co2e is null then true
        else false
    end as has_missing_emissions,

    case
        when total_emissions_kt_co2e < 0 then true
        else false
    end as has_negative_emissions,

    case
        when latitude = 0 and longitude = 0 then true
        else false
    end as has_zero_coordinates,

    case
        when city is null or trim(city) = '' then true
        else false
    end as has_missing_city,

    case
        when address is null or trim(address) = '' then true
        else false
    end as has_missing_address,

    case
        when postal_code is null 
          or trim(postal_code) = '' 
          or upper(trim(postal_code)) in ('N/A', 'NAN')
        then true
        else false
    end as has_missing_or_placeholder_postal_code

from {{ ref('stg_eccc_large_facility_emissions') }}