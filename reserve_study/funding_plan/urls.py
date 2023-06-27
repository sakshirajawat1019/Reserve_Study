from django.urls import path
from . import views

urlpatterns = [
# Module 2 
    # current funding
    path("current-funding-plan/view/<int:scenario_id>/",views.currentFundingPlan.as_view(),name="currentFundingPlan"),
    path("threshold-funding-plan/view/<int:scenario_id>/",views.ThresoldFundingPlan.as_view(),name="thresold-funding-plan"),
    path("full-funding-plan/view/<int:scenario_id>/",views.FinalFundingPlan.as_view(),name="final-funding-plan"),
    path("years-for-funding-plan/<int:scenario_id>/",views.YearsForFundingPlan.as_view(),name="YearsForFundingPlan"),
    
    # path("sign-up/",views.UserCreateView.as_view(),name= "sign-up"),
    # path("sign-in/",views.LoginAPI.as_view(),name= "sign-in")
    ]