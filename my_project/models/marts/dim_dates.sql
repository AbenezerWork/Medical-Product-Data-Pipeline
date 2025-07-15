with date_spine as (
    select distinct
        date_trunc('day', message_datetime)::date as date_day
    from {{ ref('stg_telegram_messages') }}
)
select
    date_day,
    extract(year from date_day) as year,
    extract(month from date_day) as month,
    extract(day from date_day) as day,
    extract(isodow from date_day) as day_of_week,
    to_char(date_day, 'Day') as day_name,
    to_char(date_day, 'Month') as month_name
from date_spine
