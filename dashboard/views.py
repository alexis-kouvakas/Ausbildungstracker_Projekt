import csv
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from collections import Counter


@login_required
def index(request: HttpRequest, liste="BS") -> HttpResponse:
    filename = f"Kursliste_{liste}.csv"
    file_path = os.path.join(os.path.dirname(__file__), filename)

    kurse_daten = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                kurse_daten.append(row)
    except FileNotFoundError:
        pass

    status_counts = Counter(k["Status"] for k in kurse_daten)

    context = {
        "liste": liste,
        "kurse": kurse_daten,
        "status_optionen": ["offen", "in Bearbeitung", "fertig"],
        "status_counts": dict(status_counts),
    }

    return render(request, "dashboard/index.html", context)
