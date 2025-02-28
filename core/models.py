from django.db import models

class Coach(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='coach_images')
    is_default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name