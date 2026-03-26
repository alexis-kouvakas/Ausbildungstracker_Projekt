from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class VorlageBS(models.Model):
    kursname = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False 
        db_table = 'azubi_tracker_bs' 

class VorlageDRV(models.Model):
    kursname = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'azubi_tracker_drv'


class Kurs(models.Model):
    benutzer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    Kursname = models.CharField(max_length=255)
    Status = models.CharField(max_length=50, default="offen")
    Liste = models.CharField(max_length=10)  

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.Kursname} ({self.Liste}) - {self.benutzer}"



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def weise_standard_kurse_zu(sender, instance, created, **kwargs):
    if created:
        bs_vorlagen = VorlageBS.objects.all()
        for vorlage in bs_vorlagen:
            Kurs.objects.create(
                benutzer=instance,
                Kursname=vorlage.kursname,
                Liste="BS",
                Status="offen"
            )

        drv_vorlagen = VorlageDRV.objects.all()
        for vorlage in drv_vorlagen:
            Kurs.objects.create(
                benutzer=instance,
                Kursname=vorlage.kursname,
                Liste="DRV",
                Status="offen"
            )
