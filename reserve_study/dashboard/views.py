import requests
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from funding_plan.views import calculate_current_funding, calculate_threshold_funding, calculate_full_funding
from django.db.models import F
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework import status
from scenario_management.serializers import  IntialParemetersSerializers
from scenario_management.serializers import SpecialAssessmentsSerializer,ComponentsSerializer
from scenario_management.serializers import MonthalyCommonExpensesSerializer
# from .serializers import UserSerializers,CustomTokenObtainPairSerializer
from scenario_management.models import IntialParameters
from scenario_management.models import SpecialAssessments,Components, MonthalyCommonExpenses


class ThirtyYearExpenditure(generics.GenericAPIView):
    #this api is used in dashboad for showing graph of thirty year expenditure
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IntialParemetersSerializers
    serializer_class2 = SpecialAssessmentsSerializer
    serializer_class3 = ComponentsSerializer
    serializer_class4  = MonthalyCommonExpensesSerializer

    def get(self, request, scenario_id, *args, **kwargs):

        try:
            record = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(record)
        inflation = serializer.data.get('inflation')
        try:
            record_c = Components.objects.filter(scenario_id=scenario_id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer3 = self.serializer_class3(record_c,many=True)
        component = serializer3.data

        try:
            record_of_mce = MonthalyCommonExpenses.objects.filter(scenario_id=scenario_id)
        except MonthalyCommonExpenses.DoesNotExist:

            # for adding monthly common expenses
            return Response({'error': 'Monthaly Common Expenses not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer4 = self.serializer_class4(record_of_mce,many=True)
        monthly_common_expenses = serializer4.data
        monthly_total = 0
        for rec_index in range(len(monthly_common_expenses)):
            monthly_total += (monthly_common_expenses[rec_index]["monthly_replacement_cost"]*12)

        record_SA = SpecialAssessments.objects.filter(scenario_id=scenario_id)
        serializer_of_SA = self.serializer_class2(record_SA, many = True)
        year_dataList = serializer_of_SA.data
        response = []
        i = 0 # i for calculating year number
        for record in year_dataList:
            dic = {} 
            year = record["year"]
            dic['year'] = year
            total_expenses = 0
            for rec_index in range(len(component)):
                if(component[rec_index]["Fund_component"] == "Funded"):
                    component[rec_index]["useful_life_year"] 
                    if(component[rec_index]['remaining_useful_life_years'] == 0):
                        total_expenses += int(component[rec_index]['current_replacement_cost'])
                        component[rec_index]['remaining_useful_life_years'] = component[rec_index]['useful_life_year'] - 1
                    else:
                        component[rec_index]['remaining_useful_life_years'] = component[rec_index]['remaining_useful_life_years']-1 
            dic['expenditures'] = int(total_expenses *(pow((1 + inflation / 100), i)))
            response.append(dic)
            i = i+1
        return Response(response, status=status.HTTP_200_OK)
    
    


class PercentFunded(generics.GenericAPIView):
    #this api is used in dashboad for showing graph of Percent Funded of every year
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, scenario_id, *args, **kwargs):

        try:
            current_Funding_plan = request.data.get("current_Funding_plan")
            threshold_funding_plan = request.data.get('threshold_funding_plan')
            full_funding_plan = request.data.get('full_funding_plan')

        except :
            return Response({'error': 'Please Pass Proper Payload'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            record = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = IntialParemetersSerializers(record)
       
        fiscal_year_start = serializer.data.get('fiscal_year_start')
        fiscal_year_end = serializer.data.get('fiscal_year_end')
        starting_balance = serializer.data.get('starting_balance')
        units = serializer.data.get('Number_of_units')
        cfp_annual_reserve_contribution = serializer.data.get('current_yearly_reserve_contribution')
        avg_per_unit_monthly_reserve_contribution = cfp_annual_reserve_contribution/(12*units)
        
#calculate_current_funding        
        try:
            cfp = calculate_current_funding(current_Funding_plan, scenario_id)

            cpf_response_data = cfp.data

            res1 = {
                'response_data': cpf_response_data
            }
            fully_funded_balance = cpf_response_data[0]["fully_funded_balance"]
            print(fully_funded_balance)
            cfp_result = []
            for item in res1['response_data']:
                cfp_result.append({"value":item['percent_funded'],
                            "category":item['year']
                            }
                            )
                
    #calculate_threshold_funding
            tfp = calculate_threshold_funding(threshold_funding_plan, scenario_id)
            tfp_response_data = tfp.data

            res2 = {
                'response_data': tfp_response_data
            }
            tfp_result = []
            for item in res2['response_data']:
                tfp_result.append({"value":item['percent_funded'],
                            "category":item['year']
                            }
                            )

    #calculate_full_funding
            ffp = calculate_full_funding(full_funding_plan, scenario_id)
            ffp_response_data = ffp.data


            anual_contribution = ffp_response_data[0]["reserve_contribution"]
            res3 = {
                'response_data': ffp_response_data
            }
            ffp_result = []
            for item in res3['response_data']:
                ffp_result.append({"value":item['percent_funded'],
                            "category":item['year']
                            }
                            )

                response_of_percent_funded_api = {
        "data": [
            {
                "name": "current_funding_value",
                "values": cfp_result
            },
            {
                "name": "threshold_funding_value",
                "values": tfp_result
            },
            {
                "name": "full_funding_value",
                "values": ffp_result
            }
        ]
    }
            
            response = {
                "response_of_percent_funded_api":response_of_percent_funded_api,

                "dashboard_data":{
                    "connected_communities_of_scenario":[
                        fiscal_year_start,
                        fiscal_year_end
                    ],
                    "current_year":{

                        "fiscal_year_start":fiscal_year_start,
                        "starting_balance":starting_balance,
                        "units":units,
                        "cfp_reserve_contribution":cfp_annual_reserve_contribution,
                        "fully_funded_balance":fully_funded_balance,
                        "avg_per_unit_monthly_reserve_contribution":avg_per_unit_monthly_reserve_contribution,
                        "approved_special_assessments":"No"
                        },
                    
                    "recommendations_for_next_years_reserve_contribution":{
                        "anual_contribution":anual_contribution,
                        "avg_per_unit_monthly_reserve_contribution":anual_contribution/(12*units),
                        "special_assessment_recommended": "No"
                    }
                } 
                }
            # Return a response   
            return JsonResponse( response, safe=False)
        except:
            return Response({'error': 'please give all feilds in component entry'}, status=status.HTTP_400_BAD_REQUEST)

class FundingPlansVSFullyFundedBalance(generics.GenericAPIView):
    # calculate_current_funding for Funding Plans VS FullyFunded Balance
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, scenario_id, *args, **kwargs):

        try:
            current_Funding_plan = request.data.get("current_Funding_plan")
            threshold_funding_plan = request.data.get('threshold_funding_plan')
            full_funding_plan = request.data.get('full_funding_plan')

        except :
            return Response({'error': 'Please Pass Proper Payload'}, status=status.HTTP_400_BAD_REQUEST)
        try:      
            cfp = calculate_current_funding(current_Funding_plan, scenario_id)

            cpf_response_data = cfp.data

            res1 = {
                'response_data': cpf_response_data
            }
            cfp_result = []
            ffb = []
            for item in res1['response_data']:
                cfp_result.append({"value":item['starting_balance'],
                            "category":item['year']
                            }
                            )
                ffb.append({"value":item['fully_funded_balance'],
                            "category":item['year']
                            }
                            )
                
            # calculate_threshold_funding for Funding Plans VS FullyFunded Balance    

            tfp = calculate_threshold_funding(threshold_funding_plan, scenario_id)
            tfp_response_data = tfp.data
            

            res2 = {
                'response_data': tfp_response_data
            }
            tfp_result = []
            for item in res2['response_data']:
                tfp_result.append({"value":item['starting_balance'],
                            "category":item['year']
                            }
                            )
                
            # calculate_full_funding for Funding Plans VS FullyFunded Balance 
            ffp = calculate_full_funding(full_funding_plan, scenario_id)
            ffp_response_data = ffp.data

            res3 = {
                'response_data': ffp_response_data
            }
            ffp_result = []
            for item in res3['response_data']:
                ffp_result.append({"value":item['starting_balance'],
                            "category":item['year']
                            }
                            )
            response = {
        "data": [
            {
                "name": "current_funding_value",
                "values": cfp_result
            },
            {
                "name": "threshold_funding_value",
                "values": tfp_result
            },
            {
                "name": "full_funding_value",
                "values": ffp_result
            },
            {
                "name": "fully_funded_balance",
                "values": ffb
            }
        ]
    }
        # Return a response 
            return JsonResponse(response, safe=False)
        except:
            return Response({'error': 'please give all feilds in component entry'}, status=status.HTTP_400_BAD_REQUEST)

