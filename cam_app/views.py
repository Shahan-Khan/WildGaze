from django.http import StreamingHttpResponse
from django.shortcuts import render
from .video_streamer import VideoStreamer
from cam_app.models import DetectedImage

# Create a single instance of VideoStreamer
video_streamer = VideoStreamer(source=1)

def video_stream():
    try:
        while True:
            frame_bytes = video_streamer.get_frame()
            if frame_bytes is None:
                break
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
    except KeyboardInterrupt:
        video_streamer.stop()

def video_feed(request):
    return StreamingHttpResponse(video_stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_page(request):
    # Retrieve all detected images from the database
    detected_images = DetectedImage.objects.all().order_by('-timestamp')
    
    return render(request, 'video_page.html', {'detected_images': detected_images})

def detected_images_view(request):
    # Retrieve all detected images from the database
    detected_images = DetectedImage.objects.all().order_by('-timestamp')

    # Pass the data to the template
    return render(request, 'detected_images.html', {'detected_images': detected_images})
