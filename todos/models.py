from django.db import models

from datetime import datetime
from django.db.models.fields import DateField
from django.utils import timezone


# Create your models here.


def getday():
    date = timezone.now()
    day = datetime.strftime(date,"%a-%d-%b-%Y")
    return(day)

class Todo(models.Model):
    day = models.CharField(default=getday,max_length=50)
    title = models.CharField(max_length=250)
    body = models.TextField()
    time = models.TimeField()


    def __str__(self):
        return self.day