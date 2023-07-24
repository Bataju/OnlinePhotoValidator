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
    is_jpeg = models.BooleanField(default=True)
    bgcolor_threshold = models.FloatField(default=50)
    blurness_threshold = models.FloatField(default=50)
    pixelated_threshold = models.FloatField(default=20)
    greyness_threshold = models.FloatField(default=26)
    symmetry_threshold = models.FloatField(default=20)

