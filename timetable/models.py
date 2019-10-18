from django.db import models
from data.models import Data
from django.urls import reverse
from django.conf import settings

# Create your models here.

class Timetable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    data_origin = models.ForeignKey(Data, on_delete=models.CASCADE, default=1)
    # wish_t = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='timetable_users',blank=True)
    # data_t = models.ManyToManyField(,related_name='timetable_users',blank=True)
    
    def get_absolute_url(self):
        return reverse('data:detail', kwargs={'pk': self.pk})