from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from funding_plan.views import calculate_current_funding, calculate_threshold_funding, calculate_full_funding
from django.db.models import F
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework import status
from scenario_management.serializers import  IntialParemetersSerializers,ScenarioManagementSerializers
from scenario_management.serializers import SpecialAssessmentsSerializer,ComponentsSerializer
from scenario_management.serializers import MonthalyCommonExpensesSerializer
# from .serializers import UserSerializers,CustomTokenObtainPairSerializer
from scenario_management.models import IntialParameters
from scenario_management.models import SpecialAssessments,Components, MonthalyCommonExpenses


class Expenditure(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IntialParemetersSerializers
    serializer_class2 = SpecialAssessmentsSerializer
    serializer_class3 = ComponentsSerializer
    serializer_class4  = MonthalyCommonExpensesSerializer

    def get(self, request, scenario_id, *args, **kwargs):

        try:
            record = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(record)
        inflation = serializer.data.get('inflation')
        try:
            record_c = Components.objects.filter(scenario_id=scenario_id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer3 = self.serializer_class3(record_c,many=True)
        component = serializer3.data

        try:
            record_of_mce = MonthalyCommonExpenses.objects.filter(scenario_id=scenario_id).order_by('id')
        except MonthalyCommonExpenses.DoesNotExist:
            # for adding monthly common expenses
            return Response({'error': 'Monthaly Common Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer4 = self.serializer_class4(record_of_mce,many=True)
        monthly_common_expenses = serializer4.data
        monthly_total = 0

        for rec_index in range(len(monthly_common_expenses)):
            monthly_total += (monthly_common_expenses[rec_index]["monthly_replacement_cost"]*12)

        record_SA = SpecialAssessments.objects.filter(scenario_id=scenario_id).order_by('id')
        serializer_of_SA = self.serializer_class2(record_SA, many = True)
        year_dataList = serializer_of_SA.data
        response = []
        i = 0

        for component_data in component:
            if component_data["Fund_component"] == "Funded":
                component_name = component_data["Component_title"]
                component_expenses = []

                for record in year_dataList:
                    year = record["year"]
                    expenses = 0

                    if component_data['remaining_useful_life_years'] == 0:
                        total_expenses = int(component_data['current_replacement_cost'])
                        expenses = total_expenses * pow((1 + inflation / 100), i)
                        component_data['remaining_useful_life_years'] = component_data['useful_life_year'] - 1
                    else:
                        component_data['remaining_useful_life_years'] -= 1

                    component_expenses.append({'year': year, 'expense': expenses})

                response.append({'component': component_name, 'values': component_expenses})
        return Response(response, status=status.HTTP_200_OK)

