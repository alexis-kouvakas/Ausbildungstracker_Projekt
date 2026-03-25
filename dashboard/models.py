from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- 1. DEINE BESTEHENDEN VORLAGEN (Nur zum Lesen) ---

class VorlageBS(models.Model):
    # Die Spaltennamen müssen exakt so heißen wie in deiner Datenbank
    kursname = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False  # WICHTIG: Sagt Django "Fass diese Tabelle nicht an, sie existiert schon!"
        db_table = 'azubi_tracker_bs' # Der exakte Name deiner Tabelle in Postgres

class VorlageDRV(models.Model):
    kursname = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'azubi_tracker_drv'


# --- 2. DIE PERSÖNLICHEN KURSE DER AZUBIS (Hier wird der Fortschritt gespeichert) ---

class Kurs(models.Model):
    # Verknüpfung zum jeweiligen Azubi
    benutzer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    Kursname = models.CharField(max_length=255)
    Status = models.CharField(max_length=50, default="offen")
    Liste = models.CharField(max_length=10)  # "BS" oder "DRV"

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.Kursname} ({self.Liste}) - {self.benutzer}"


# --- 3. DER AUTOMATISMUS BEIM ERSTELLEN EINES BENUTZERS ---

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def weise_standard_kurse_zu(sender, instance, created, **kwargs):
    # Wenn der Benutzer gerade ganz neu erstellt wurde...
    if created:
        # 1. Alle Kurse aus der BS-Tabelle holen und für den Azubi kopieren
        bs_vorlagen = VorlageBS.objects.all()
        for vorlage in bs_vorlagen:
            Kurs.objects.create(
                benutzer=instance,
                Kursname=vorlage.kursname,
                Liste="BS",
                Status="offen"
            )

        # 2. Alle Kurse aus der DRV-Tabelle holen und für den Azubi kopieren
        drv_vorlagen = VorlageDRV.objects.all()
        for vorlage in drv_vorlagen:
            Kurs.objects.create(
                benutzer=instance,
                Kursname=vorlage.kursname,
                Liste="DRV",
                Status="offen"
            )
