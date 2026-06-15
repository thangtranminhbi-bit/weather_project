WITH source AS (
    SELECT * FROM {{source('weather_tables', 'weather_final')}}
),
renamed AS (
    SELECT
    CAST(timestamp AS timestamp) weather_timestamp,
    CAST(timestamp AS DATE) weather_date,
    EXTRACT(HOUR FROM CAST(timestamp AS timestamp)) weather_hour,
    CAST(temperature AS FLOAT64) temperature_celsius,
    CAST(humidity AS FLOAT64) humidity_percentage,
    ingested_at
    FROM source
)
SELECT * FROM renamed