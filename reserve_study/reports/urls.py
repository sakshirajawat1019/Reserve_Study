from django.urls import path
from .views import generate_pdf

urlpatterns = [
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    # Other URL patterns...
]
