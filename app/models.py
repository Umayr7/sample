import string

from PIL.ImagePath import Path
from django.db import models
from PIL import Image
import os

class ImageCompress(models.Model):
    image = models.ImageField(default=None, upload_to='photos')

    def __str__(self):
        return f'photo to compress'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
