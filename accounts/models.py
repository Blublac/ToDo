from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from django.db.models.deletion import DO_NOTHING

# Create your models here.class CustomUser(AbstractUser):
    
class CustomUser(AbstractUser):
    address = models.TextField()
    id= models.UUIDField(primary_key=True, unique=True, editable=False,default=uuid.uuid4)
    