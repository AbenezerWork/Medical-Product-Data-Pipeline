with detections as (
    select * from {{ ref('stg_image_detections') }}
)

select
    -- We can use a surrogate key if a single message has multiple detections
    {{ dbt_utils.generate_surrogate_key(['message_id', 'detected_object_class']) }} as detection_id,
    message_id,
    detected_object_class,
    confidence_score
from detections
