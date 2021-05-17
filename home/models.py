from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# modele baza de date

class Sign(models.Model):
    sign_id = models.IntegerField(default=0 , primary_key = True)
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='signs')

    def __str__(self):
        return self.name
  

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User , on_delete=models.CASCADE)
    sign_id = models.ForeignKey(Sign , on_delete=models.CASCADE)
    recognition_date = models.DateTimeField(default=timezone.now)
    #loss = models.FloatField(default=0)
    accuracy= models.FloatField(default=0)
    #recognition_time =  models.FloatField(default=0)

    def __str__(self):
        return self.event_id

class ReportBug(models.Model):
    title = models.CharField(max_length=100)
    bug = models.ImageField(upload_to='report')
    description = models.TextField()
    
        
    def __str__(self):
        return self.title






