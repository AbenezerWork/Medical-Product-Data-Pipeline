with source as (
    -- Reference the raw table created by the Python script
    select *,
           row_number() over (partition by (data ->> 'id')::bigint order by loaded_at desc) as rn
    from {{ source('raw', 'telegram_messages') }}
),

renamed as (
    select
        -- Extract top-level fields from the JSONB 'data' column
        (data ->> 'id')::bigint as message_id,
        (data ->> 'date')::timestamptz as message_datetime,
        (data ->> 'message') as message_text,
        (data ->> 'views')::integer as message_views,
        
        -- Extract nested channel information
        (data -> 'peer_id' ->> 'channel_id')::bigint as channel_id,
        
        -- Check if an image path exists (from our Python script)
        (data ->> 'image_path') is not null as has_image,
        
        loaded_at as loaded_at_utc

    from source
    where rn = 1
)

select * from renamed
