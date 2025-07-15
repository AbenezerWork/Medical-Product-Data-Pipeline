with messages as (
    select * from {{ ref('stg_telegram_messages') }}
),

channels as (
    select * from {{ ref('dim_channels') }}
),

dates as (
    select * from {{ ref('dim_dates') }}
)

select
    -- Surrogate Key
    messages.message_id,
    
    -- Foreign Keys
    messages.channel_id,
    dates.date_day,
    
    -- Message Metrics
    messages.message_text,
    length(messages.message_text) as message_length,
    messages.message_views,
    messages.has_image,
    messages.message_datetime

from messages
left join dates on date_trunc('day', messages.message_datetime)::date = dates.date_day
