from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from collections import Counter
from .models import Kurs 

@login_required
def index(request: HttpRequest, liste="BS") -> HttpResponse:
    if liste not in ["BS", "DRV"]:
        return HttpResponse("Liste nicht gefunden", status=404)

    if request.method == "POST":
        kurse_db = Kurs.objects.filter(Liste=liste, benutzer=request.user).order_by('id')
        for kurs in kurse_db:
            neuer_status = request.POST.get(f"status_{kurs.Kursname}")
            if neuer_status and neuer_status != kurs.Status:
                kurs.Status = neuer_status
                kurs.save()
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
