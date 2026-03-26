from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('logout/', views.logout_user, name='logout'),
    path('gesamtansicht/', views.gesamtansicht, name='gesamtansicht'),
    path("<str:liste>/", views.index, name="kursliste")
]
