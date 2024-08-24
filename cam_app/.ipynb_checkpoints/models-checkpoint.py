#from django.db import models

# Create your models here.

# class AnimalClass(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

# class DetectedImage(models.Model):
#     image = models.ImageField(upload_to='detected_objects/')
#     animal_class = models.ForeignKey(AnimalClass, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.animal_class.name} detected at {self.timestamp}"

#--------------------------------------------------------------------------------
from django.db import models

class AnimalClass(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DetectedImage(models.Model):
    image = models.ImageField(upload_to='detected_objects/')
    animal_class = models.ForeignKey(AnimalClass, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.animal_class.name} detected at {self.timestamp}"

    @property
    def timestamp_without_seconds(self):
        return self.timestamp.replace(second=0, microsecond=0)

class EnvData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    jsonData = models.JSONField()

    def __str__(self):
        return f"EnvData at {self.timestamp}"

from django.db import models
from django.utils import timezone

class EnvironmentalData(models.Model):
    data = models.JSONField() 
    timestamp = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return f"EnvironmentalData {self.id} at {self.timestamp}"



