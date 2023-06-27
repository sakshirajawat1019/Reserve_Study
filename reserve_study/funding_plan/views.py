import requests
import math
from django.db.models import F
from rest_framework import generics,permissions
from rest_framework.response import Response
from rest_framework import status
from scenario_management.serializers import  IntialParemetersSerializers, SpecialAssessmentsSerializer
from scenario_management.serializers import ComponentsSerializer,MonthalyCommonExpensesSerializer
from scenario_management.models import IntialParameters,SpecialAssessments
from scenario_management.models import Components, MonthalyCommonExpenses


############################################################ Module -2 ###################################
# ######################################################## Funding Plan API ##############################


#this function used in multiple module api dashboad, funding plan and component detail 
def calculate_current_funding(data,scenario_id):

    try:
        reserve_contribution = data.get('reserve_contribution')
        special_assessments = data.get('special_assessments')
        first_year = reserve_contribution["first_year"]
        percentage_change = reserve_contribution['percentage_change']
        default_value = reserve_contribution['default_value']
        custom_value = reserve_contribution['custom_value']
    except :
        return Response({'error': 'Please pass proper payload'}, status=status.HTTP_404_NOT_FOUND)

    try:
        record = IntialParameters.objects.get(scenario_id=scenario_id)
    except IntialParameters.DoesNotExist:
        return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = IntialParemetersSerializers(record)
    starting_balance = serializer.data.get('starting_balance')
    inflation = serializer.data.get('inflation')
    reserve_contribution = serializer.data.get('current_yearly_reserve_contribution')
    try:
        record_c = Components.objects.filter(scenario_id=scenario_id).order_by('id')
    except Components.DoesNotExist:
        return Response({'error': 'Component not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer3 = ComponentsSerializer(record_c,many=True)
    component = serializer3.data
    fully_funded_balance = 0
    percent_funded = 0
    interest_earned = 0
    try:
        record_of_mce = MonthalyCommonExpenses.objects.filter(scenario_id=scenario_id).order_by('id')
    except MonthalyCommonExpenses.DoesNotExist:
        return Response({'error': 'Monthaly Common Expenses not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer4 = MonthalyCommonExpensesSerializer(record_of_mce,many=True)
    monthly_common_expenses = serializer4.data
    monthly_total = 0
    for rec_index in range(len(monthly_common_expenses)):
        monthly_total += (monthly_common_expenses[rec_index]["monthly_replacement_cost"]*12)
    record_SA = SpecialAssessments.objects.filter(scenario_id=scenario_id).order_by('id')
    serializer_of_SA = SpecialAssessmentsSerializer(record_SA, many = True)
    year_dataList = serializer_of_SA.data
    total_cost = 0
    response = []
    i = 0
    for record in year_dataList:
        dic = {} 
        year = record["year"]
        amount = record["amount"]
        dic['year'] = year
        dic['starting_balance'] = starting_balance
        dic['reserve_contribution'] = reserve_contribution
        if(percentage_change == "Uniform"):
            if((first_year == True and i==0)):
                dic['percent_change'] = 0
            else:
                dic['percent_change'] = default_value  
        else:
            if(len(custom_value)== 30):
                if((first_year == True and i==0)):
                    dic['percent_change'] = 0
                else:
                    dic['percent_change'] = custom_value[i]  
            else:
                return Response("gives all 30 custom value", status=status.HTTP_404_NOT_FOUND)
        dic['special_assessments'] = amount
        dic['interest_earned'] = interest_earned
        total_expenses = 0
        total_cost = 0
        val = 0
        fully_funded_balance = 0
        
        for rec_index in range(len(component)): 
            
            if(component[rec_index]["Fund_component"] == "Funded"):
                
                try:
                    val = ((component[rec_index]["useful_life_year"]-component[rec_index]['remaining_useful_life_years'])/component[rec_index]["useful_life_year"])
                except:
                    return Response({'error': 'useful_life_year not found in component'}, status=status.HTTP_404_NOT_FOUND)
                if(component[rec_index]['remaining_useful_life_years'] == 0):
                    total_expenses += int(component[rec_index]['current_replacement_cost'])
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['useful_life_year'] - 1
                else:
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['remaining_useful_life_years']-1
               
                val = val*int(component[rec_index]['current_replacement_cost'])
                total_cost += val
                inflation = 2
                # import pdb; pdb.set_trace()
                if(int(component[rec_index]['current_replacement_cost'])!=0):
                    fully_funded_balance =round(total_cost*(pow((1 + inflation / 100), i))) 
                    
        if(fully_funded_balance == 0):
            return Response({'error': 'Please fill all details in component'}, status=status.HTTP_404_NOT_FOUND)         
        dic['expenditures'] = int(total_expenses + monthly_total *(pow((1 + inflation / 100), i)))
        dic["ending_balance"] = int(starting_balance) + int(reserve_contribution) + dic['special_assessments'] + int(interest_earned) - dic['expenditures'] 
        dic['fully_funded_balance'] = fully_funded_balance
        dic['percent_funded'] = (100*dic['starting_balance'] )/fully_funded_balance
        starting_balance = dic["ending_balance"]
        reserve_contribution = int(((dic['percent_change']*reserve_contribution)/100)+reserve_contribution)
        response.append(dic)
        i = i+1
    return Response(response, status=status.HTTP_200_OK)


def calculate_threshold_funding(data, scenario_id):
    #this function calculate threshold function in funding plan
    try:
        min_end_balance_expend_ratio = data.get("min_end_balance_expend_ratio")
        reserve_contribution = data.get('reserve_contribution')
        special_assessments = data.get('special_assessments')
        
        first_year = True
        percentage_change = reserve_contribution['percentage_change']
        custom_value = reserve_contribution['custom_value']
        default_min_value = reserve_contribution['default_min_value']
        default_max_value = reserve_contribution['default_max_value']
        
        min_ending_balance_year = special_assessments['min_ending_balance_year']
        specialAssessments_added_for_years = special_assessments['specialAssessments_added_for_years']
        funding_priority = special_assessments['funding_priority']

    except :
        return Response({'error': 'Please pass proper payload'}, status=status.HTTP_404_NOT_FOUND)
    try:
        record = IntialParameters.objects.get(scenario_id=scenario_id)
    except IntialParameters.DoesNotExist:
        return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = IntialParemetersSerializers(record)
    starting_balance = serializer.data.get('starting_balance')
    inflation = serializer.data.get('inflation')
    reserve_contribution = serializer.data.get('current_yearly_reserve_contribution')
    try:
        record_SA = Components.objects.filter(scenario_id=scenario_id).order_by('id')
    except Components.DoesNotExist:
        return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer3 = ComponentsSerializer(record_SA,many=True)
    component = serializer3.data
    fully_funded_balance = 0
    percent_funded = 0
    interest_earned = 0
    record = SpecialAssessments.objects.filter(scenario_id=scenario_id).order_by('id')
    serializer_of_SA = SpecialAssessmentsSerializer(record, many = True)
    year_dataList = serializer_of_SA.data
    response = []
    i = 0
    for record in year_dataList:
        dic = {} 
        year = record["year"]
        amount = record["amount"]
        dic['year'] = year
        dic['starting_balance'] = starting_balance
        dic['reserve_contribution'] = reserve_contribution
        if(percentage_change == "Uniform"):
            if((first_year == True and i==0)):
                dic['percent_change'] = 0
            else:
                dic['percent_change'] = default_min_value  
        else:
            dic['percent_change'] = 0
            # if(len(custom_value)== 30):
            #     if((first_year == True and i==0)):
            #         dic['percent_change'] = 0
            #     else:
            #         dic['percent_change'] = custom_value[i]  
            # else:
            #     return Response("gives all 30 custom value", status=status.HTTP_404_NOT_FOUND)
        

        dic['special_assessments'] = amount
        dic['interest_earned'] = interest_earned
        total_expenses = 0
        total_cost = 0
        val = 0
        fully_funded_balance = 0
        for rec_index in range(len(component)):
            if(component[rec_index]["Fund_component"] == "Funded"):
                try:
                    val = ((component[rec_index]["useful_life_year"]-component[rec_index]['remaining_useful_life_years'])/component[rec_index]["useful_life_year"])
                except:
                    return Response({'error': 'useful_life_year not found in component'}, status=status.HTTP_404_NOT_FOUND) 
                if(component[rec_index]['remaining_useful_life_years'] == 0):
                    total_expenses += int(component[rec_index]['current_replacement_cost'])
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['useful_life_year'] - 1
                else:
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['remaining_useful_life_years']-1 
                
                # cal fully_funded_balance
                val = val*int(component[rec_index]['current_replacement_cost'])
                total_cost += val
                # inflation = 2
                if(int(component[rec_index]['current_replacement_cost'])!=0):
                    fully_funded_balance =round(total_cost*(pow((1 + inflation / 100), i))) 

        if(fully_funded_balance == 0):
            return Response({'error': 'Please fill all details in component'}, status=status.HTTP_404_NOT_FOUND)             
        dic['expenditures'] = int(total_expenses *(pow((1 + inflation / 100), i)))
        dic["ending_balance"] = int(starting_balance) + int(reserve_contribution) + dic['special_assessments'] + int(interest_earned) - dic['expenditures'] 
        dic['fully_funded_balance'] = fully_funded_balance
        dic['percent_funded'] = (100*dic['starting_balance'] )/(dic['fully_funded_balance'])
        starting_balance = dic["ending_balance"]
        reserve_contribution = int(((dic['percent_change']*reserve_contribution)/100)+reserve_contribution)
        response.append(dic)
        i = i+1

    
    return Response(response, status=status.HTTP_200_OK)

def calculate_full_funding(data, scenario_id):
    
    try:
        min_end_balance_expend_ratio = data.get("min_end_balance_expend_ratio")
        reserve_contribution = data.get('reserve_contribution')
        special_assessments = data.get('special_assessments')
        minimal_percent_funded_last_year = data.get('minimal_percent_funded_last_year')
        
        first_year = True
        percentage_change = reserve_contribution['percentage_change']
        efault_min_value = reserve_contribution['default_min_value']
        default_max_value = reserve_contribution['default_max_value']
        custom_value = reserve_contribution['custom_value']
        
        min_ending_balance_year = special_assessments['min_ending_balance_year']
        specialAssessments_added_for_years = special_assessments['specialAssessments_added_for_years']
        funding_priority = special_assessments['funding_priority']
    except :
        return Response({'error': 'Please pass proper payload'}, status=status.HTTP_404_NOT_FOUND)

    try:
        record = IntialParameters.objects.get(scenario_id=scenario_id)
    except IntialParameters.DoesNotExist:
        return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = IntialParemetersSerializers(record)
    starting_balance = serializer.data.get('starting_balance')
    inflation = serializer.data.get('inflation')
    reserve_contribution = serializer.data.get('current_yearly_reserve_contribution')
    try:
        record_SA = Components.objects.filter(scenario_id=scenario_id).order_by('id')
    except Components.DoesNotExist:
        return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer3 = ComponentsSerializer(record_SA,many=True)
    component = serializer3.data
    fully_funded_balance = 0
    percent_funded = 0
    interest_earned = 0
    record = SpecialAssessments.objects.filter(scenario_id=scenario_id).order_by('id')
    serializer_of_SA = SpecialAssessmentsSerializer(record, many = True)
    year_dataList = serializer_of_SA.data
    response = []
    count = 0
    for record in year_dataList:
        dic = {} 
        year = record["year"]
        amount = record["amount"]
        dic['year'] = year
        dic['starting_balance'] = starting_balance
        dic['reserve_contribution'] = reserve_contribution
        if(percentage_change == "Uniform"):
            if((first_year == True and count==0)):
                dic['percent_change'] = 0
            else:
                dic['percent_change'] = efault_min_value  
        # else:
            # if(len(custom_value)== 30):
            #     if((first_year == True and i==0)):
            #         dic['percent_change'] = 0
            #     else:
            #         dic['percent_change'] = custom_value[i]  
            # else:
            #     return Response("gives all 30 custom value", status=status.HTTP_404_NOT_FOUND)
        dic['special_assessments'] = amount
        dic['interest_earned'] = interest_earned
        total_expenses = 0
        total_cost = 0
        val = 0
        fully_funded_balance = 0
        for rec_index in range(len(component)):
            if(component[rec_index]["Fund_component"] == "Funded"):
                try:
                    val = ((component[rec_index]["useful_life_year"]-component[rec_index]['remaining_useful_life_years'])/component[rec_index]["useful_life_year"])
                except:
                    return Response({'error': 'useful_life_year not found in component'}, status=status.HTTP_404_NOT_FOUND)
                if(component[rec_index]['remaining_useful_life_years'] == 0):
                    total_expenses += int(component[rec_index]['current_replacement_cost'])
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['useful_life_year'] - 1
                else:
                    component[rec_index]['remaining_useful_life_years'] = component[rec_index]['remaining_useful_life_years']-1 
            # cal fully_funded_balance
                val = val*int(component[rec_index]['current_replacement_cost'])
                total_cost += val
                inflation = 2
                if(int(component[rec_index]['current_replacement_cost'])!=0):
                    fully_funded_balance =round(total_cost*(pow((1 + inflation / 100), count)))

        if(fully_funded_balance == 0):
            return Response({'error': 'Please fill all details in component'}, status=status.HTTP_404_NOT_FOUND) 
        dic['expenditures'] = int(total_expenses *(pow((1 + inflation / 100), count)))
        dic["ending_balance"] = int(starting_balance) + int(reserve_contribution) + dic['special_assessments'] + int(interest_earned) - dic['expenditures'] 
        dic['fully_funded_balance'] = fully_funded_balance
        dic['percent_funded'] = percent_funded
        starting_balance = dic["ending_balance"]
        # reserve_contribution = int(((dic['percent_change']*reserve_contribution)/100)+reserve_contribution)
        response.append(dic)
        count = count+1
    return Response(response, status=status.HTTP_200_OK)  


class currentFundingPlan(generics.GenericAPIView):
    ## calculate current funding plan for funding plan module
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, scenario_id, *args, **kwargs):
        data = request.data
        return calculate_current_funding(data, scenario_id)

class ThresoldFundingPlan(generics.GenericAPIView):
    # calculate threshold funding plan for funding plan module
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, scenario_id, *args, **kwargs):
        data = request.data
        return calculate_threshold_funding(data, scenario_id)
            
class FinalFundingPlan(generics.GenericAPIView):
    # calculate fulll funding plan for funding plan module
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, scenario_id, *args, **kwargs):
        data = request.data
        return calculate_full_funding(data, scenario_id)

class YearsForFundingPlan(generics.GenericAPIView):
    # this api used to show drop down list of year in full fundig plan and threshold api
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SpecialAssessmentsSerializer

    def get(self, request, scenario_id, *args, **kwargs):
        record = SpecialAssessments.objects.filter(scenario_id=scenario_id).order_by('id')
        if not record:
            return Response({'error': 'Special Assessments years are not found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer_of_SA = self.serializer_class(record, many = True)
        year_dataList = serializer_of_SA.data
        
        first_year = int(year_dataList[0]["year"].split("-")[0])
        last_year = int(year_dataList[-1]["year"].split("-")[1])
        response = []
        j = 1  #for increamenting year
        for i in range(first_year,last_year):
            year = str(first_year)+"-"+str(first_year+j)
            List_year = year
            j = j+1
            response.append(List_year)

        print(response)
         
        return Response(response, status=status.HTTP_200_OK) 
