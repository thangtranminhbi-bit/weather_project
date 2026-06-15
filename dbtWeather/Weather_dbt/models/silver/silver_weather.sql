with staging as (
      select * from {{ ref('bronze_weather') }}
  ),
  enriched as (
      select
          *,
          case 
              when temperature_celsius > 35 then 'Hot'
              when temperature_celsius < 22 then 'Cool'
              else 'Normal'
          end as temperature_status
      from staging
  )
  select * from enriched