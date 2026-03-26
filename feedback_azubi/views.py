from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import FeedbackFormular
from dashboard.models import Kurs

def index(request, kurs_id):
    aktueller_kurs = get_object_or_404(Kurs, id=kurs_id)
    anzeigename = aktueller_kurs.Kursname if aktueller_kurs.Kursname else f"Kurs #{aktueller_kurs.id}"
    
    context = {
        'kurs': aktueller_kurs,
        'anzeigename': anzeigename
    }
    return render(request, "feedback_azubi/index.html", context)

def submit_feedback(request):
    if request.method == 'POST':
        FeedbackFormular.objects.create(
            dozentenname=request.POST.get('kursleitung'),
            kurs_id=request.POST.get('kursname'),
            kursnummer=request.POST.get('lehrgangsnummer'),
            zufriedenheitswert=request.POST.get('bewertung_kurs'),
            allgemeiner_bewertungswert=request.POST.get('bewertung_kurs'),
            kompetenzwert=request.POST.get('kompetenz_dozent'),
            ilias_modul_bewertung=request.POST.get('ilias_modul'),
            selbsteinschaetzungswert=request.POST.get('selbsteinschaetzung'),
            sonstiges=request.POST.get('anmerkungen')
        )
        return redirect('/dashboard/DRV/')
    
    return redirect('/dashboard/DRV/')
