from django.db import models


class Image(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image = models.FileField(upload_to='img/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
