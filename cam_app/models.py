from django.db import models

# Create your models here.

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
