# Generated by Django 4.2.15 on 2024-08-12 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DetectedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='detected_objects/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('animal_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cam_app.animalclass')),
            ],
        ),
    ]
