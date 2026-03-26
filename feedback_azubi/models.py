from django.db import models
from dashboard.models import Kurs
# Create your models here.

class FeedbackFormular(models.Model):

    dozentenname = models.CharField(max_length=50)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, db_column='kursname')
    kursnummer = models.CharField(max_length=20)
    zufriedenheitswert = models.IntegerField()
    allgemeiner_bewertungswert = models.IntegerField()
    kompetenzwert = models.IntegerField()
    ilias_modul_bewertung = models.IntegerField()
    selbsteinschaetzungswert = models.IntegerField()
    sonstiges = models.TextField(blank=True, null=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback_formular'

    def __str__(self):
        return f"Feedback für Kurs-ID {self.kurs.Kursname} von {self.dozentenname}"
