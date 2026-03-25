from django.db import models

# Create your models here.
 class Kurs(models.Model):
    Kursname = models.CharField(max_length=255)
    Status = models.CharField(max_length=50, default="offen")
    Liste = models.CharField(max_length=10)  # Hier speichern wir "BS" oder "DRV"

    def __str__(self):
        return f"{self.Kursname} ({self.Liste})"
