import requests
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.db.models import F
from rest_framework import generics,permissions
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from funding_plan.views import calculate_current_funding, calculate_threshold_funding, calculate_full_funding
from scenario_management.serializers import UnitsIfVariableSerializer,IntialParemetersSerializers,ComponentsSerializer
from scenario_management.models import Components,IntialParameters,UnitsIfVariable


class CurrentFundingPlan(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, scenario_id, *args, **kwargs ):
        # this api used in componentDetail of current funding plan
        try:
            record_of_components = Components.objects.filter(scenario_id=scenario_id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer3 = ComponentsSerializer(record_of_components,many=True)
        component = serializer3.data

        try:
            record_of_initial_pera = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_of_initial_pera = IntialParemetersSerializers(record_of_initial_pera)
        reserve_contribution = serializer_of_initial_pera.data.get('current_yearly_reserve_contribution')
        starting_balance = serializer_of_initial_pera.data.get('starting_balance')
        fixed_reserve_contribution =reserve_contribution
        variable_reserve_contribution = reserve_contribution
        total_reserve_contribution = reserve_contribution


        try:
            record_of_unit = UnitsIfVariable.objects.filter(scenario_id=scenario_id).order_by('id')
            # import pdb; pdb.set_trace()
        except UnitsIfVariable.DoesNotExist:
            return Response({'error': 'Units not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitsIfVariableSerializer(record_of_unit, many=True)
        units_detail = serializer.data



    #ByIndividualComponent API
        fully_funded_balance = 0
        response_of_ByIndividualComponent = []
        for record in component:
            dic = {} 
            component_title = record["Component_title"]
            useful_life = record["useful_life_year"]
            remaining_useful_life = record["remaining_useful_life_years"]
            replacement_cost = record["current_replacement_cost"]
            dic['component_title'] = component_title
            dic['useful_life'] = useful_life
            dic['remaining_useful_life'] = remaining_useful_life
            dic['replacement_cost'] = replacement_cost
            dic['fully_funded_balance'] = fully_funded_balance
            dic['yearly_cost'] = 0
            dic['funded_balance'] = starting_balance
            dic['reserve_contribution'] = reserve_contribution
            response_of_ByIndividualComponent.append(dic)

    #BYComponentCategory
        components = serializer3.data
        
        category = set()
        response_of_BYComponentCategory = []
        
        for record in components:
            category.add(record["category"])
        
        for cat in category:
            useful_life_list = []
            remaining_useful_life_list = []
            replacement_cost_list = []
            
            for record in components:

                if record["category"] == cat:
                    # print(record)  # Added this line to print the record dictionary
                    useful_life_list.append(int(record["useful_life_year"]))
                    remaining_useful_life_list.append(int(record["remaining_useful_life_years"]))
                    replacement_cost_list.append(int(record["current_replacement_cost"]))
            
            useful_life_max = max(useful_life_list) 
            useful_life_min = min(useful_life_list)
            remaining_useful_life_max = max(remaining_useful_life_list)
            remaining_useful_life_min = min(remaining_useful_life_list)
            replacement_cost_max = max(replacement_cost_list)
            replacement_cost_min = min(replacement_cost_list)

            
            response_of_BYComponentCategory.append({
                "category": cat,
                "useful_life": f"{useful_life_min}-{useful_life_max}",
                "remaining_useful_life": f"{remaining_useful_life_min}-{remaining_useful_life_max}",
                "replacement_cost": f"{replacement_cost_min}-{replacement_cost_max}",
                "fully_funded_balance": 0,
                "yearly_cost": 0,
                "funded_balance": starting_balance,
                "reserve_contribution": reserve_contribution
            })


       # Byunits
        units_list = []
        building_list = []
        address_list = []
        square_footage_list = []
        percentage_list = []
        response_of_Byunits = []
        fixed_rc_list = []
        variable_rc_list = []
        total_rc_list = []
        

        for data in units_detail:
            unit_dic = {}
            units_list.append(data["unit"])
            building_list.append(int(data["building"]))
            address_list.append(data["address"])
            square_footage_list.append(int(data["square_footage"]))
            percentage_list.append(int(data["percentage"]))
            fixed_rc_list.append(int(fixed_reserve_contribution))
            variable_rc_list.append(int(variable_reserve_contribution))
            total_rc_list.append(int(total_reserve_contribution))
            unit_dic['unit'] = data["unit"]
            unit_dic['building'] = data["building"]
            unit_dic['address'] = data["address"]
            unit_dic['square_footage'] = data["square_footage"]
            unit_dic['percentage'] = data["percentage"]
            unit_dic['fixed_reserve_contribution'] = fixed_reserve_contribution
            unit_dic['variable_reserve_contribution'] = variable_reserve_contribution
            unit_dic['total_reserve_contribution'] = variable_reserve_contribution
            response_of_Byunits.append(unit_dic)


        response = {
                "current_funding_plan":{
                "response_of_ByIndividualComponent":response_of_ByIndividualComponent,
                "response_of_BYComponentCategory":response_of_BYComponentCategory,
                "response_of_Byunits":response_of_Byunits
            }
            }

        return Response(response, status=status.HTTP_200_OK)

class ThresholdFundingPlan(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, scenario_id, *args, **kwargs ):
        # this api used in componentDetail of threshold funding plan

        try:
            record_of_components = Components.objects.filter(scenario_id=scenario_id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer3 = ComponentsSerializer(record_of_components,many=True)
        component = serializer3.data

        try:
            record_of_initial_pera = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_of_initial_pera = IntialParemetersSerializers(record_of_initial_pera)
        reserve_contribution = serializer_of_initial_pera.data.get('current_yearly_reserve_contribution')
        starting_balance = serializer_of_initial_pera.data.get('starting_balance')
        fixed_reserve_contribution =reserve_contribution
        variable_reserve_contribution = reserve_contribution
        total_reserve_contribution = reserve_contribution

        try:
            record_of_unit = UnitsIfVariable.objects.filter(scenario_id=scenario_id).order_by('id')
        except UnitsIfVariable.DoesNotExist:
            return Response({'error': 'Units not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitsIfVariableSerializer(record_of_unit, many=True)
        units_detail = serializer.data



    #ByIndividualComponent API
        fully_funded_balance = 0
        response_of_ByIndividualComponent = []
        for record in component:
            dic = {} 
            component_title = record["Component_title"]
            useful_life = record["useful_life_year"]
            remaining_useful_life = record["remaining_useful_life_years"]
            replacement_cost = record["current_replacement_cost"]
            dic['component_title'] = component_title
            dic['useful_life'] = useful_life
            dic['remaining_useful_life'] = remaining_useful_life
            dic['replacement_cost'] = replacement_cost
            dic['fully_funded_balance'] = fully_funded_balance
            dic['yearly_cost'] = 0
            dic['funded_balance'] = starting_balance
            dic['reserve_contribution'] = reserve_contribution
            response_of_ByIndividualComponent.append(dic)


    #BYComponentCategory
        components = serializer3.data
        
        category = set()
        response_of_BYComponentCategory = []
        
        for record in components:
            category.add(record["category"])
        
        for cat in category:
            useful_life_list = []
            remaining_useful_life_list = []
            replacement_cost_list = []
            
            for record in components:

                if record["category"] == cat:
                    # print(record)  # Added this line to print the record dictionary
                    useful_life_list.append(int(record["useful_life_year"]))
                    remaining_useful_life_list.append(int(record["remaining_useful_life_years"]))
                    replacement_cost_list.append(int(record["current_replacement_cost"]))
            
            useful_life_max = max(useful_life_list) 
            useful_life_min = min(useful_life_list)
            remaining_useful_life_max = max(remaining_useful_life_list)
            remaining_useful_life_min = min(remaining_useful_life_list)
            replacement_cost_max = max(replacement_cost_list)
            replacement_cost_min = min(replacement_cost_list)

            
            response_of_BYComponentCategory.append({
                "category": cat,
                "useful_life": f"{useful_life_min}-{useful_life_max}",
                "remaining_useful_life": f"{remaining_useful_life_min}-{remaining_useful_life_max}",
                "replacement_cost": f"{replacement_cost_min}-{replacement_cost_max}",
                "fully_funded_balance": 0,
                "yearly_cost": 0,
                "funded_balance": starting_balance,
                "reserve_contribution": reserve_contribution
            })


        # Byunits
        units_list = []
        building_list = []
        address_list = []
        square_footage_list = []
        percentage_list = []
        response_of_Byunits = []
        fixed_rc_list = []
        variable_rc_list = []
        total_rc_list = []
        

        for data in units_detail:
            unit_dic = {}
            units_list.append(data["unit"])
            building_list.append(int(data["building"]))
            address_list.append(data["address"])
            square_footage_list.append(int(data["square_footage"]))
            percentage_list.append(int(data["percentage"]))
            fixed_rc_list.append(int(fixed_reserve_contribution))
            variable_rc_list.append(int(variable_reserve_contribution))
            total_rc_list.append(int(total_reserve_contribution))
            unit_dic['unit'] = data["unit"]
            unit_dic['building'] = data["building"]
            unit_dic['address'] = data["address"]
            unit_dic['square_footage'] = data["square_footage"]
            unit_dic['percentage'] = data["percentage"]
            unit_dic['fixed_reserve_contribution'] = fixed_reserve_contribution
            unit_dic['variable_reserve_contribution'] = variable_reserve_contribution
            unit_dic['total_reserve_contribution'] = variable_reserve_contribution
            response_of_Byunits.append(unit_dic)

        response = {
                "threshold_funding_plan":{
                "response_of_ByIndividualComponent":response_of_ByIndividualComponent,
                "response_of_BYComponentCategory":response_of_BYComponentCategory,
                "response_of_Byunits":response_of_Byunits
            }
            }

        return Response(response, status=status.HTTP_200_OK)  


class FullFundingPlan(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, scenario_id, *args, **kwargs ):
        # this api used in componentDetail of full funding plan

        try:
            record_of_components = Components.objects.filter(scenario_id=scenario_id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer3 = ComponentsSerializer(record_of_components,many=True)
        component = serializer3.data

        try:
            record_of_initial_pera = IntialParameters.objects.get(scenario_id=scenario_id)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Scenario not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer_of_initial_pera = IntialParemetersSerializers(record_of_initial_pera)
        reserve_contribution = serializer_of_initial_pera.data.get('current_yearly_reserve_contribution')
        starting_balance = serializer_of_initial_pera.data.get('starting_balance')
        fixed_reserve_contribution =reserve_contribution
        variable_reserve_contribution = reserve_contribution
        total_reserve_contribution = reserve_contribution


        try:
            record_of_unit = UnitsIfVariable.objects.filter(scenario_id=scenario_id).order_by('id')
            # import pdb; pdb.set_trace()
        except UnitsIfVariable.DoesNotExist:
            return Response({'error': 'Units not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UnitsIfVariableSerializer(record_of_unit, many=True)
        units_detail = serializer.data



    #ByIndividualComponent API
        fully_funded_balance = 0
        response_of_ByIndividualComponent = []
        for record in component:
            dic = {} 
            component_title = record["Component_title"]
            useful_life = record["useful_life_year"]
            remaining_useful_life = record["remaining_useful_life_years"]
            replacement_cost = record["current_replacement_cost"]
            dic['component_title'] = component_title
            dic['useful_life'] = useful_life
            dic['remaining_useful_life'] = remaining_useful_life
            dic['replacement_cost'] = replacement_cost
            dic['fully_funded_balance'] = fully_funded_balance
            dic['yearly_cost'] = 0
            dic['funded_balance'] = starting_balance
            dic['reserve_contribution'] = reserve_contribution
            response_of_ByIndividualComponent.append(dic)


    #BYComponentCategory
        components = serializer3.data
        
        category = set()
        response_of_BYComponentCategory = []
        
        for record in components:
            category.add(record["category"])
        
        for cat in category:
            useful_life_list = []
            remaining_useful_life_list = []
            replacement_cost_list = []
            
            for record in components:

                if record["category"] == cat:
                    # print(record)  # Added this line to print the record dictionary
                    useful_life_list.append(int(record["useful_life_year"]))
                    remaining_useful_life_list.append(int(record["remaining_useful_life_years"]))
                    replacement_cost_list.append(int(record["current_replacement_cost"]))
            
            useful_life_max = max(useful_life_list) 
            useful_life_min = min(useful_life_list)
            remaining_useful_life_max = max(remaining_useful_life_list)
            remaining_useful_life_min = min(remaining_useful_life_list)
            replacement_cost_max = max(replacement_cost_list)
            replacement_cost_min = min(replacement_cost_list)

            
            response_of_BYComponentCategory.append({
                "category": cat,
                "useful_life": f"{useful_life_min}-{useful_life_max}",
                "remaining_useful_life": f"{remaining_useful_life_min}-{remaining_useful_life_max}",
                "replacement_cost": f"{replacement_cost_min}-{replacement_cost_max}",
                "fully_funded_balance": 0,
                "yearly_cost": 0,
                "funded_balance": starting_balance,
                "reserve_contribution": reserve_contribution
            })


    # Byunits
        units_list = []
        building_list = []
        address_list = []
        square_footage_list = []
        percentage_list = []
        response_of_Byunits = []
        fixed_rc_list = []
        variable_rc_list = []
        total_rc_list = []
        

        for data in units_detail:
            unit_dic = {}
            units_list.append(data["unit"])
            building_list.append(int(data["building"]))
            address_list.append(data["address"])
            square_footage_list.append(int(data["square_footage"]))
            percentage_list.append(int(data["percentage"]))
            fixed_rc_list.append(int(fixed_reserve_contribution))
            variable_rc_list.append(int(variable_reserve_contribution))
            total_rc_list.append(int(total_reserve_contribution))
            unit_dic['unit'] = data["unit"]
            unit_dic['building'] = data["building"]
            unit_dic['address'] = data["address"]
            unit_dic['square_footage'] = data["square_footage"]
            unit_dic['percentage'] = data["percentage"]
            unit_dic['fixed_reserve_contribution'] = fixed_reserve_contribution
            unit_dic['variable_reserve_contribution'] = variable_reserve_contribution
            unit_dic['total_reserve_contribution'] = variable_reserve_contribution
            response_of_Byunits.append(unit_dic)

        response = {
                "full_funding_plan":{
                "response_of_ByIndividualComponent":response_of_ByIndividualComponent,
                "response_of_BYComponentCategory":response_of_BYComponentCategory,
                "response_of_Byunits":response_of_Byunits
            }
            }

        return Response(response, status=status.HTTP_200_OK)      
       

           