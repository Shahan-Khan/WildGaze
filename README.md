# WildGaze

WildGaze is a real-time animal detection and monitoring system that uses computer vision and artificial intelligence to detect and monitor animals in real time. 
The system continuously captures video feeds and employs the YOLOv7-tiny model, trained on a custom dataset, to identify specific animals. 

Detected animals are automatically captured and stored in the database with the image, timestamp, and environmental data (temperature, pressure, humidity) via a Sense HAT.

This allows users to access and review detected images with timestamps and environmental conditions remotely. Additionally, WildGaze supports real-time video streaming over a network.

## Installation

1. **Create a virtual environment**
    ```bash
    python -m venv venv
    ```
2. **Activate the virtual environment**

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ``` 
3. **Install OpenCV and Django**
    ```bash
    pip install opencv-python django
    ```
4. **Clone the YOLOv7 repository**
    ```bash
    git clone https://github.com/your-username/yolov7.git
    cd yolov7
    ```

5. **Install YOLOv7 Requirements**
    ```bash
    pip install -r requirements.txt
    ```
6. **Clone the WildGaze repository**
    ```bash
    git clone https://github.com/your-username/wildGaze.git
    cd wildGaze
    ```
7. **Run the Django app**
    ```bash
    python manage.py runserver
    ```
