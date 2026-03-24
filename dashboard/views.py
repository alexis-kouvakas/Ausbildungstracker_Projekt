import csv
import os
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

@login_required
def index(request: HttpRequest, liste='BS') -> HttpResponse:
    filename = f'Kursliste_{liste}.csv'
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    kurse_daten = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            # DictReader nutzt die Kopfzeile (Kursname, Status) als Keys
            reader = csv.DictReader(csvfile)
            for row in reader:
                kurse_daten.append(row)
    except FileNotFoundError:
        pass

    context = {
        'liste': liste,
        'kurse': kurse_daten,
        'status_optionen': ['offen', 'in Bearbeitung', 'fertig']
    }
    
    return render(request, "dashboard/index.html", context)