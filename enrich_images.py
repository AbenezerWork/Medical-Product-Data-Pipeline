import os
import json
import logging
from datetime import datetime
from ultralytics import YOLO

# --- Configuration & Setup ---

# Define data storage paths
TODAY = datetime.now().strftime('%Y-%m-%d')
RAW_IMAGES_DIR = os.path.join('data', 'raw', 'telegram_images', TODAY)
ENRICHED_OUTPUT_DIR = os.path.join('data', 'enriched', TODAY)

# Create directories if they don't exist
os.makedirs(ENRICHED_OUTPUT_DIR, exist_ok=True)

# Logging Setup
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')


def enrich_images_with_yolo():
    """Scans for new images, runs YOLOv8 detection, and saves the results."""
    logging.info("--- Starting Image Enrichment with YOLOv8 ---")

    # Load a pre-trained YOLOv8 model
    try:
        model = YOLO('yolov8x.pt')
        logging.info("YOLOv8 model loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load YOLOv8 model: {e}")
        return

    # Check if the image directory exists
    if not os.path.exists(RAW_IMAGES_DIR):
        logging.warning(f"Image directory not found: {RAW_IMAGES_DIR}. No images to process.")
        return

    all_detections = []

    # Process each image in the directory
    for image_name in os.listdir(RAW_IMAGES_DIR):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(RAW_IMAGES_DIR, image_name)

            try:
                # Run object detection
                results = model(image_path)

                # Extract message_id from the image filename
                message_id = int(os.path.splitext(image_name)[0])

                # Process detection results
                for result in results:
                    for box in result.boxes:
                        detection = {
                            'message_id': message_id,
                            'detected_object_class_id': int(box.cls),
                            'detected_object_class_name': model.names[int(box.cls)],
                            'confidence_score': float(box.conf),
                            'timestamp': datetime.now().isoformat()
                        }
                        all_detections.append(detection)

                logging.info(f"Processed image: {image_name}")

            except Exception as e:
                logging.error(f"Failed to process image {image_name}: {e}")

    # Save all detections to a single JSON file
    if all_detections:
        output_path = os.path.join(
            ENRICHED_OUTPUT_DIR, 'image_detections.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_detections, f, ensure_ascii=False, indent=4)
        logging.info(f"Saved {len(all_detections)} detections to {output_path}")

    logging.info("--- Image Enrichment Finished ---")


if __name__ == "__main__":
    enrich_images_with_yolo()
