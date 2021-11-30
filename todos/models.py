from django.db import models

from datetime import datetime
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import DateField
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()




# Create your models here.


def getday():
    date = timezone.now()
    day = datetime.strftime(date,"%a-%d-%b-%Y")
    return(day)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=DO_NOTHING,related_name='to_do',null=True,blank=True)
    day = models.CharField(default=getday,max_length=50,editable=False)
    activity = models.TextField()
    time = models.TimeField()
    completed = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.day



    def delete(self):
        self.is_active = False
        self.save()
        return
