import cv2
import threading
import time
import torch
from django.core.files import File
from django.conf import settings
import os
from cam_app.models import AnimalClass, DetectedImage

class VideoStreamer:
    def __init__(self, source=0, confidence_threshold=0.7, save_interval=3):
        self.cap = cv2.VideoCapture(source)
        self.lock = threading.Lock()
        self.frame = None
        self.is_running = True

        # Create directory to save detected images
        # os.makedirs(save_dir, exist_ok=True)
        # self.save_dir = save_dir

        # Load the YOLOv7-tiny model
        self.model = torch.hub.load('WongKinYiu/yolov7', 'custom', path_or_model='/home/astranode/my_space/yolo/best.pt')

        # Get class names from the model
        self.class_names = self.model.names

        # Set the confidence threshold
        self.confidence_threshold = confidence_threshold

        # Minimum time between saves in seconds
        self.save_interval = save_interval
        self.last_save_time = time.time()

        threading.Thread(target=self.update_frame, daemon=True).start()

    def update_frame(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                self.is_running = False
                break

            # Resize frame for faster processing
            frame = cv2.resize(frame, (640, 480))

            # Perform object detection
            results = self.model(frame)

            # Filter results based on confidence threshold
            detections = results.xyxy[0]
            detections = detections[detections[:, 4] >= self.confidence_threshold]

            # Render the results on the frame
            current_time = time.time()
            for i, (xmin, ymin, xmax, ymax, confidence, class_idx) in enumerate(detections):
                # Convert coordinates to integer
                xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)

                # Draw bounding box and label on the frame
                label = f"{self.class_names[int(class_idx)]}: {confidence:.2f}"
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                # Check if enough time has passed since the last save
                if current_time - self.last_save_time >= self.save_interval:
                    # Crop the detected object from the frame
                    # object_img = frame[ymin:ymax, xmin:xmax]

                    # Generate a filename for the detected object
                    timestamp = int(time.time())
                    filename = f'detected_{self.class_names[int(class_idx)]}_{timestamp}_{i}.jpg'
                    file_path = os.path.join(settings.MEDIA_ROOT, 'detected_objects', filename)

                    # Create directory if it doesn't exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                    # Save the cropped object image
                    cv2.imwrite(file_path, frame)

                    # Save the detected image and class to the database
                    animal_name = self.class_names[int(class_idx)]
                    animal_class, created = AnimalClass.objects.get_or_create(name=animal_name)

                    relative_path = os.path.join('detected_objects', filename)
                    DetectedImage.objects.create(image=relative_path, animal_class=animal_class)

                    # Update the last save time
                    self.last_save_time = current_time

            with self.lock:
                self.frame = frame

    def get_frame(self):
        with self.lock:
            if self.frame is not None:
                ret, jpeg = cv2.imencode('.jpg', self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if ret:
                    return jpeg.tobytes()
            return None

    def stop(self):
        self.is_running = False
        self.cap.release()

