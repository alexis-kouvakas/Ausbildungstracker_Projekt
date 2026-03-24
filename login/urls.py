from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
]

urlpatterns = [
    path("", views.login_prompt, name="login"),
]
