from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField(max_length=50)