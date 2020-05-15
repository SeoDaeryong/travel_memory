from django.db import models


# Create your models here.
class ImageInfo(models.Model):
    spot = models.IntegerField()
    image = models.ImageField(blank=False, upload_to='images/')
    revision = models.IntegerField(default=0)
    main = models.IntegerField(default=0)
