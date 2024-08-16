from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# URLConf
urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('video_page/', views.video_page, name='video_page'),
    path('detected-images/', views.detected_images_view, name='detected_images'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)