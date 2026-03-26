from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from collections import Counter
from .models import Kurs
from django.contrib.auth import logout

@login_required
def gesamtansicht(request):
    kurse = Kurs.objects.filter(benutzer=request.user).order_by('Liste', 'id')
    raw_counts = Counter(kurs.Status for kurs in kurse)
    status_counts = {
        "offen": raw_counts.get("offen", 0),
        "in_bearbeitung": raw_counts.get("in Bearbeitung", 0),
        "abgeschlossen": raw_counts.get("abgeschlossen", 0),
    }
    context = {
        "kurse": kurse,
        "status_counts": status_counts,
        "aktuelle_liste": "gesamtansicht",
    }
    return render(request, "dashboard/gesamtansicht.html", context)

def index(request: HttpRequest, liste="BS") -> HttpResponse:
    if liste not in ["BS", "DRV"]:
        return HttpResponse("Liste nicht gefunden", status=404)

    if request.method == "POST":
        kurse_db = Kurs.objects.filter(Liste=liste, benutzer=request.user).order_by('id')
        feedback_kurs_id = None

        for kurs in kurse_db:
            neuer_status = request.POST.get(f"status_{kurs.Kursname}")
            if neuer_status and neuer_status != kurs.Status:
                if neuer_status == "abgeschlossen" and kurs.Liste == "DRV":
                    feedback_kurs_id = kurs.id
                
                kurs.Status = neuer_status
                kurs.save()
        
        if feedback_kurs_id:
            return redirect('feedback_form', kurs_id=feedback_kurs_id)

        return redirect(request.path)

    kurse_db = Kurs.objects.filter(Liste=liste, benutzer=request.user).order_by('id')

    raw_counts = Counter(kurs.Status for kurs in kurse_db)

    status_counts = {
        "offen": raw_counts.get("offen", 0),
        "in_bearbeitung": raw_counts.get("in Bearbeitung", 0),
        "abgeschlossen": raw_counts.get("abgeschlossen", 0),
    }

    context = {
        "aktuelle_liste": liste,
        "kurse": kurse_db,
        "status_counts": status_counts,
    }
    return render(request, "dashboard/index.html", context)

def logout_user(request):
    logout(request)
    return redirect('/login/')
