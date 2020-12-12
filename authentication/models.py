from django.db import models

# Create your models here.
class OTP(models.Model):
    sender = models.CharField(max_length=500)   
    value = models.CharField(max_length=500)
    def __str__(self):
        return self.sender