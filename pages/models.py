from django.db import models

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = "Qr_image"

class AdvImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='imgAdv')
    class Meta:
        db_table = "Qr_imageAdv"