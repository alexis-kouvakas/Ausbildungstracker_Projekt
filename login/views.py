from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_prompt(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard/")
        else:
            return render(
                request, "login/login.html", {"error": "Falsche Zugangsdaten"}
            )
    return render(request, "login/login.html")
