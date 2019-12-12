from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
# Create your models here.

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_profile = ProcessedImageField(
                upload_to='user_profile/images',                
                processors=[ResizeToFill(300, 300)],     
                format='JPEG',                           
                options={'quality':90},                 
                blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    age = models.IntegerField(default=1,validators=[MaxValueValidator(100),MinValueValidator(1)],blank=True,null=True)
    gender_choice = [['M','남성'],['F','여성']]
    gender = models.CharField(max_length=1,choices=gender_choice,blank=True,null=True)
    
    
    def get_absolute_url(self):
        return reverse('user_profile:base')