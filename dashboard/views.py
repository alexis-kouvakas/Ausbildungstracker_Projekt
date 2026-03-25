from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from collections import Counter

# HIER MUSST DU DEINE ECHTEN KLASSENNAMEN AUS DER models.py EINTRAGEN!
# Ich nenne sie jetzt beispielhaft KursBS und KursDRV
from .models import KursBS, KursDRV


@login_required
def index(request: HttpRequest, liste="BS") -> HttpResponse:

    # --- 1. Die richtige Tabelle für die aktuelle Seite auswählen ---
    if liste == "BS":
        AktuellesModel = KursBS
    elif liste == "DRV":
        AktuellesModel = KursDRV
    else:
        # Fallback, falls mal eine falsche URL aufgerufen wird
        return HttpResponse("Liste nicht gefunden", status=404)

    # --- 2. POST: Wenn der "Speichern" Knopf gedrückt wurde ---
    if request.method == "POST":
        kurse_db = AktuellesModel.objects.all()

        for kurs in kurse_db:
            # Wir suchen nach dem passenden Dropdown-Namen aus dem HTML
            # WICHTIG: Wenn deine Spalte in der DB anders heißt als "Kursname" oder "Status",
            # musst du das hier (.Kursname / .Status) anpassen!
            neuer_status = request.POST.get(f"status_{kurs.Kursname}")

            # Hat sich der Status geändert? Dann in Postgres speichern!
            if neuer_status and neuer_status != kurs.Status:
                kurs.Status = neuer_status
                kurs.save()

        # Nach dem Speichern die Seite einfach neu laden
        return redirect(request.path)

    # --- 3. GET: Daten für die Anzeige aus Postgres holen ---
    kurse_daten = AktuellesModel.objects.all()
    status_counts = Counter(k.Status for k in kurse_daten)

    context = {
        "liste": liste,
        "kurse": kurse_daten,
        "status_optionen": ["offen", "in Bearbeitung", "fertig"],
        "status_counts": dict(status_counts),
    }

    return render(request, "dashboard/index.html", context)
