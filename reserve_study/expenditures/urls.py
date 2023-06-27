from django.urls import path
from . import views

urlpatterns = [
    path("view/<int:scenario_id>/",views.Expenditure.as_view(),name="expenditure_detail"),
    ]