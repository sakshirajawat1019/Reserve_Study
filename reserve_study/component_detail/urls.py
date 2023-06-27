from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    # path("view/<int:scenario_id>/",views.ComponentDetail.as_view(),name="component_detail"),
    path("current-funding-plan/view/<int:scenario_id>/",views.CurrentFundingPlan.as_view(),name="component_detail"),
    path("threshold-funding-plan/view/<int:scenario_id>/",views.ThresholdFundingPlan.as_view(),name="component_detail"),
    path("full-funding-plan/view/<int:scenario_id>/",views.FullFundingPlan.as_view(),name="component_detail")
    ]