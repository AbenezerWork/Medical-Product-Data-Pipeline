select
    (data ->> 'message_id')::bigint as message_id,
    (data ->> 'detected_object_class_name') as detected_object_class,
    (data ->> 'confidence_score')::numeric as confidence_score
from {{ source('raw', 'image_detections') }}
