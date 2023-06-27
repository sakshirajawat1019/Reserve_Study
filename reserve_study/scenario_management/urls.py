from django.urls import path
from scenario_management import views

urlpatterns = [
    path('create/', views.SMCreateAPIView.as_view(), name="create"),
    path('update/<int:id>/', views.SMUpdateAPIView.as_view(), name='update_scenario'),
    path('delete/<int:pk>/',views.DeleteScenarioManagement.as_view(),name = "DeleteScenarioManagement"),
    path('view-scenarios/',views.ListAPIView.as_view(), name="view_scenarios"), 
    path('view-scenarios/<int:id>/',views.GetScenarioManagement.as_view(), name="view_scenarios"),
    path('update-active-field/<int:id>/',views.UpdateActiveFieldView.as_view(),name="update_active_field"),
    # path('scenario_management/view_scenario_name/', views.get_scenario_name.as_view(), name="get_scenario_name"),  
    path('locks-scenario/<int:id>/',views.LockScenario.as_view(),name="Lock_Scenario"),

    # intial_parameter  
    path("intial-parameter/view/",views.IntialPerameterList.as_view(),name="Intial_perameter_list"),
    path("intial-parameter/view/<int:id>/", views.GetIntialPerameter.as_view(),name="Intial_perameter_list_view"),
    path("intial-parameter/update/<int:pk>/",views.IntialPerameterUpdate.as_view(),name="Intial_perameter_update"),
    # path("intial_parameter/delete/<int:pk>/",views.IntialPerameterDelete.as_view(),name="organisation_delete"), 

    # Units_If_Variabl API
    path("units-if-variable/view/",views.ListUnitsIfVariableAPIView.as_view(),name="UnitsIf_vriable_list"),
    path("units-if-variable/view/<int:id>/",views.GetnitsIfVariableAPIView.as_view(),name="UnitsIfVariable"),
    path("units-if-variable/create-or-update/", views.createORupdateUnitsIfVariableAPIView.as_view(),name="UnitsIfVariable_create"),
    # path("Units_If_Variable/update/<int:id>/",views.createOrUpdateUnitsIfVariable.as_view(),name="UnitsIfVariable_update"),
    path("units-if-variable/delete/<int:pk>/",views.DeleteUnitsIfVariableAPIView.as_view(),name="UnitsIfVariable_delete"), 

    # SpecialAssessmentsList
    path("special-assessments/view/",views.SpecialAssessmentsList.as_view(),name="get_special_assessments_list"),
    path("special-assessments/view/<int:id>/",views.GetSpecialAssessments.as_view(),name="get_special_Assessments"),
    path("special-assessments/update/",views.SpecialAssessmentsUpdate.as_view(),name="update_get_special_assessments"),

    path("components/view/",views.ComponentsList.as_view(),name="get_components_list"),
    path("components/view/<int:id>/",views.GetComponents.as_view(),name="get_components"),
    path("components/update/",views.ComponentsCreateOrUpdate.as_view(),name="update_components"),
    path("components/create-or-update/",views.ComponentsCreateOrUpdate.as_view(),name="CreateOrupdate_components"),
    path("componenets/download-csv/<int:id>/",views.ComponenetCsv.as_view(),name="component_csv"),
    # path("/componenets/uploadCsv/<int:id>/",views.ComponenetUploadCsv.as_view(),name="component_csv"),
    
    path("loan-other-expenditures/view/<int:id>/",views.GetLoanOtherExpenditures.as_view(),name="get_LoanOtherExpenditures"),
    path("loan-other-expenditures/update-or-create/",views.createORupdateLoanOtherExpenditures.as_view(),name="update_components"),
   
    path("monthaly-common-expenses/view/",views.MonthalyCommonList.as_view(), name="MonthalyCommon_List"),
    path("monthaly-common-expenses/view/<int:id>/",views.GetMonthalyCommon.as_view(),name="MonthalyCommon_List_data"),
    path("monthaly-common-expenses/create-or-update/",views.MonthalyCommonCreateOrUpdate.as_view(),name="MonthalyCommon_CreateAndUpdate"),
    path("monthaly-common-expenses/status/<int:scenario_id>/",views.UnactiveMonthlyExpendeture.as_view(),name="MonthalyCommon_Status")

    #  path("access-user",views.GetAccessUserAPIView.as_view(),name="user access for scenario managment")

]