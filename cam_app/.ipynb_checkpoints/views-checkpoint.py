from django.http import StreamingHttpResponse
from django.shortcuts import render
from .video_streamer import VideoStreamer
from cam_app.models import DetectedImage

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from .models import EnvData
import json

from django.db.models import F, OuterRef, Subquery
from django.db.models.functions import Abs

# Create a single instance of VideoStreamer
video_streamer = VideoStreamer(source=0)

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
    
    images_with_data = []

    # Loop through detected images to find the closest EnvironmentalData
    for image in detected_images:
        # Get the closest EnvironmentalData entry
        closest_environmental_data = (
            EnvironmentalData.objects
            .filter(timestamp__lte=image.timestamp)
            .order_by('-timestamp')
            .first()
        )
        
        images_with_data.append({
            'image': image,
            'environmental_data': closest_environmental_data
        })

    # Prepare the context to send to the template
    context = {
        'images_with_data': images_with_data,
    }

    return render(request, 'video_page.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import EnvironmentalData

@csrf_exempt
def SaveEnvironmentalData(request):
    if request.method == 'POST':
        # try:
        data = json.loads(request.body)
        environmental_data = EnvironmentalData(data=data)
        environmental_data.save()

        return JsonResponse({'status': 'success', 'message': 'Data saved successfully'}, status=201)
        # except json.JSONDecodeError:
            # return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
def ShowEnvironmentalData(request):
    data = EnvironmentalData.objects.all()
    return render(request, 'show_data.html', {'data': data})
