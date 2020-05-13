from django.db import models


# Create your models here.
class ImageInfo(models.Model):
    spot = models.IntegerField()
    image = models.ImageField(blank=False, upload_to='images/')