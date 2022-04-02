from email.policy import default
from operator import mod
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='download.png', upload_to='profile_image')
    birthday = models.DateField(auto_now=False, null=True)
    phone = models.CharField(max_length = 20, null=True)
    country = models.CharField(max_length = 50, null=True)
    city = models.CharField(max_length = 30, null = True)
    address = models.CharField(max_length = 255, null=True)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
