with intermediate as (
    select * from {{ ref('silver_weather') }}
),
daily_summary as (
    select
        weather_date,
        count(weather_hour) as hours_recorded,
        round(avg(temperature_celsius), 2) as avg_temperature,
        max(temperature_celsius) as max_temperature,
        min(temperature_celsius) as min_temperature,
        round(avg(humidity_percentage), 2) as avg_humidity
    from intermediate
    group by weather_date
)
select * from daily_summary