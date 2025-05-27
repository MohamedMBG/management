from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Superviseur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='superviseur')
    telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(default=timezone.now)

    @property
    def nom(self):
        return self.user.last_name

    @property
    def prenom(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    class Meta:
        verbose_name = "Superviseur"
        verbose_name_plural = "Superviseurs"
        ordering = ['-date_ajout']