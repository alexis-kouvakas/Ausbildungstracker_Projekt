from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required  # 1. Importieren


# Create your views here.
@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/index.html")
