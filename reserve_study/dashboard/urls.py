from django.urls import path
from . import views

urlpatterns = [
# Module 2 
    # current funding   
    path("thirty-year-expenditure/<int:scenario_id>/",views.ThirtyYearExpenditure.as_view(),name="ThirtyYearExpenditure"),
    path("percent-funded/<int:scenario_id>/",views.PercentFunded.as_view(),name="PercentFunded"),
    path("funding-plans-vs-fully-funded-balance/<int:scenario_id>/",views.FundingPlansVSFullyFundedBalance.as_view(),name="FundingPlansVSFullyFundedBalance")
    # path("sign-up/",views.UserCreateView.as_view(),name= "sign-up"),
    ]