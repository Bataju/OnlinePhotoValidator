from django.db import models

# Create your models here.
class Config(models.Model):
    min_height = models.FloatField()
    max_height = models.FloatField()
    min_width = models.FloatField()
    max_width = models.FloatField()
    min_size = models.FloatField()
    max_size = models.FloatField()
    is_jpg = models.BooleanField()
    is_png = models.BooleanField()
    image = models.ImageField(upload_to='images/')

