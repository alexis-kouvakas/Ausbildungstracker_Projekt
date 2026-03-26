from django.urls import path
from . import views 
from django.views.generic import RedirectView

urlpatterns = [
    path('<int:kurs_id>', views.index, name='feedback_form'),
    path('submit/', views.submit_feedback, name='submit_feedback'),
]
