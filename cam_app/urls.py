from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import SaveEnvironmentalData
from .views import ShowEnvironmentalData

# URLConf
urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('SaveEnvironmentalData/', SaveEnvironmentalData, name='SaveEnvironmentalData'),
    path('video_page/', views.video_page, name='video_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)