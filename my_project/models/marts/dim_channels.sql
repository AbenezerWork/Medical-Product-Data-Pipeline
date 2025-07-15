with message_source as (
    select * from {{ ref('stg_telegram_messages') }}
)

select distinct
    channel_id,
    -- In a real project, you would join this with another source
    -- that contains the channel names. For now, we'll use the ID as the name.
    'Channel ' || channel_id::text as channel_name
from message_source
where channel_id is not null
