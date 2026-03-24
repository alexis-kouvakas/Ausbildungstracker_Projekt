from django.urls import path
from . import views

urlpatterns = [
    path("<str:liste>/", views.index, name="kursliste"),
    path("", views.index, name="index"),
]
