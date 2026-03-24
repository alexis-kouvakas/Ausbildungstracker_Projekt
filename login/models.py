# login/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Azubi(AbstractUser):

    class Meta:
        verbose_name = 'Azubi'
        verbose_name_plural = 'Azubis'

    def __str__(self):
        return self.username
