from django.db import models

class HomePageImage(models.Model):
    image = models.ImageField(upload_to='home_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Home Page Image"
