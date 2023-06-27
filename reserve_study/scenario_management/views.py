import requests
from django.shortcuts import render,HttpResponse,get_object_or_404
from django.http import JsonResponse
import csv
from django.utils.encoding import smart_str
from django.db.models import F
from rest_framework import generics,permissions
from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScenarioManagementSerializers, IntialParemetersSerializers
from .serializers import UnitsIfVariableSerializer,SpecialAssessmentsSerializer,ComponentsSerializer
from .serializers import LoanOtherExpendituresSerializer,MonthalyCommonExpensesSerializer
# from .serializers import UserSerializers,CustomTokenObtainPairSerializer
from .serializers import ComponenetCsvSwaggerSerializer
from .models import ScenarioManagement,IntialParameters,UnitsIfVariable,CustomUser
from .models import SpecialAssessments,Components, LoanOtherExpenditures, MonthalyCommonExpenses
# from accounts.models import AccessUser
# from accounts.serializers import AccessUserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
import jwt
from django.conf import settings

class SMCreateAPIView(generics.GenericAPIView):
    """
        Desc: for creating scenario for scenario managment model inital perameter and special assessment
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers
    def post(self, request):
        token = request.headers.get('Authorization')
        if token:
            try:
                token = token.split(' ')[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                # Use the user ID as needed
            except (jwt.exceptions.DecodeError, KeyError):
                return JsonResponse({'error': 'Invalid token'}, status=400)
        else:
            return JsonResponse({'error': 'Token missing'}, status=400)
        
        try:
            data = request.data
            copy = data.get('copy')
            
            if(copy == True):
                original_instance = ScenarioManagement.objects.get(active= True)
                Scenario_Name = original_instance.scenario_name+" (copy)"
                last_Saved_By = CustomUser.objects.get(id = user_id)
                created_by = CustomUser.objects.get(id = user_id)
                new_instance = ScenarioManagement(**{
                'last_saved_by':last_Saved_By,
                'scenario_name': Scenario_Name ,
                'notes':original_instance.notes,
                'status':True,
                'created_by':created_by,
                })
                new_instance.save()
                serializer = self.serializer_class(new_instance)
                return Response({
                'message': 'Data stored successfully',
                'data': serializer.data
                })
            else :
            
                count = ScenarioManagement.objects.count()
                Scenario_Name = "New Scenario" + str(count+1)
                last_Saved_By = CustomUser.objects.get(id = user_id)
                created_by = CustomUser.objects.get(id = user_id)
                print(created_by)
                new_instance = ScenarioManagement(**{
                'last_saved_by':last_Saved_By,
                'scenario_name': Scenario_Name,
                'notes':"None",
                'status':True,
                
                'created_by':created_by
                })
                new_instance.save()
                serializer = self.serializer_class(new_instance)
                
                initial_perameter = self.create_initial_perameter(new_instance)
                Special_assessments = self.create_Special_assessments(new_instance)
                # components = self.create_components(new_instance)
                return Response({
                'message': 'Data stored successfully',
                'data': serializer.data,
                'initial_perameter':initial_perameter,
                'Special_assessments':Special_assessments,
                # 'components':components
                })
        except Exception as e:
            return Response({'message': str(e)})

    serializer_class2 = IntialParemetersSerializers

    def create_initial_perameter(self, scenario_instance_id):
        # this function create by default intial perameter
        try:
            ip = IntialParameters.objects.create(scenario_id=scenario_instance_id)
            ip.save()
            serializer2 = self.serializer_class2(ip)
            return serializer2.data
        except Exception as e:
            return str(e)

      
    def create_Special_assessments(self, scenario_instance_id):
        serializer_class3 = SpecialAssessmentsSerializer 
        # this function create by default special assessment
        try:
            ip2 = IntialParameters.objects.get(scenario_id = scenario_instance_id)
            serializer_class2 = IntialParemetersSerializers
            sc = self.serializer_class2 (ip2)
            start_date = int(sc.data['fiscal_year_start'].split('-')[0])
            for i in range(30):
                date1 = start_date+i
                date2 = date1 + 1
                year_range = str(date1)+"-"+str(date2)
                new_instance = SpecialAssessments(**{
            'scenario_id': scenario_instance_id,
            'year':year_range
            })
                new_instance.save()
                serializer3 = serializer_class3(new_instance)
            return serializer3.data
        except Exception as e:
            return str(e) 
        
    # serializer_class_of_CS = ComponentsSerializer
    # def create_components(self, scenario_instance_id):
    #     try:
    #         # import pdb;pdb.set_trace()
    #         ip = Components.objects.create(scenario_id=scenario_instance_id)
    #         ip.save()
    #         cs_serializer = self.serializer_class_of_CS(ip)
    #         return cs_serializer.data
    #     except Exception as e:
    #         return str(e)       


class GetScenarioManagement(generics.GenericAPIView):
    """
        Desc: for getting particular record by id or primary key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers
    def get(self, request,id):
        
        try:
            queryset = ScenarioManagement.objects.get(id=id)
            serializer = self.get_serializer(queryset)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)})     
        
        
class SMUpdateAPIView(generics.GenericAPIView):
    """
        Desc: for updating scenario managment record 
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers

    def put(self, request, *args, **kwargs):
        
        token = request.headers.get('Authorization')
        if token:
            try:
                token = token.split(' ')[1]
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                self.grant_access(request,user_id)
                # Use the user ID as needed
            except (jwt.exceptions.DecodeError, KeyError):
                return JsonResponse({'error': 'Invalid token'}, status=400)
        else:
            return JsonResponse({'error': 'Token missing'}, status=400)
        
        try:
            
            last_Saved_By = CustomUser.objects.get(id = 2)
            instance = self.get_object()
            instance.last_saved_by = last_Saved_By
            # instance.save()
            serializer = self.get_serializer(instance, data=request.data)
            # import pdb;
            # pdb.set_trace()
            serializer.is_valid(raise_exception=True)
            
            serializer.save()

            return Response({
            'message': 'Data updated successfully',
            'data': serializer.data
            })
        except Exception as e:
            return Response({'message': str(e)})
        

        
        
    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs.get('id'))
        return obj

    def get_queryset(self):
        return ScenarioManagement.objects.all()


class ListAPIView(generics.GenericAPIView):
    """
        Desc: for viewing all records of scenario managment 
    """
    # import pdb;
    # pdb.set_trace()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers
    queryset = ScenarioManagement.objects.all()

    def get(self, request, *args, **kwargs):
        user = request.user
        # print(user)
        # import pdb; 
        # pdb.set_trace()
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    

class DeleteScenarioManagement(generics.DestroyAPIView):
    """
    Desc: for Deleting scenario by giving primary key(id) from scenario management model
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = ScenarioManagement.objects.all()
    serializer_class = ScenarioManagementSerializers 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Scenario deleted successfully."}, status=status.HTTP_200_OK)


class UpdateActiveFieldView(generics.GenericAPIView):
    """
        Desc: for updating active scenario from scenario managment model

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers 
    def put(self, request, id):
        try:
            ScenarioManagement.objects.update(active=False)
            instance = ScenarioManagement.objects.get(id=id)
            instance.active = True
            instance.save()
            serializer = self.serializer_class(instance)
            return Response(serializer.data)
        except ScenarioManagement.DoesNotExist:
            return Response({'message': 'ScenarioManagement instance does not exist'})
        except Exception as e:
            return Response({'message': str(e)})   
        


class LockScenario(generics.GenericAPIView):
    """
        Desc: for Lock Scenario active from scenario managment model

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers 
    def put(self, request, id):
        try:
            data = request.data
            status = data.get('status')
            if(status == True):
                # ScenarioManagement.objects.update(active=False)
                instance = ScenarioManagement.objects.get(id=id)
                instance.status = False
                instance.save()
                serializer = self.serializer_class(instance)
                return Response(serializer.data)
        except ScenarioManagement.DoesNotExist:
            return Response({'message': 'ScenarioManagement instance does not exist'})
        except Exception as e:
            return Response({'message': str(e)})         



 ##################################################   intial perameter API    #######################################
class IntialPerameterList(ListAPIView):
    """
    This endpoint list all of the available Intial Perameter record from the database
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = IntialParameters.objects.all()
    serializer_class = IntialParemetersSerializers

#delete api
class IntialPerameterCreate(CreateAPIView):
    """
    This endpoint allows for creation of a Intial Perameter record
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = IntialParameters.objects.all()
    serializer_class = IntialParemetersSerializers

class GetIntialPerameter(generics.GenericAPIView):
    """
        Desc: for getting particular record by scenario_id or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IntialParemetersSerializers
    def get(self, request,id):
        try:
            queryset = IntialParameters.objects.get(scenario_id=id)
            serializer = self.get_serializer(queryset)
            return Response({
            'data': [serializer.data],
            })
        except Exception as e:
            return Response({'message': str(e)})  
        
class IntialPerameterUpdate(generics.GenericAPIView):
    """
    This endpoint allows for updating a specific Intial Perameter record by passing in the id of the todo to update
    """
    permission_classes = [permissions.IsAuthenticated]
    # queryset = IntialParameters.objects.all()
    serializer_class = IntialParemetersSerializers   
    def put(self, request, pk): 
        try:
            instance = IntialParameters.objects.get(id=pk)
        except IntialParameters.DoesNotExist:
            return Response({'error': 'Initial Perameter is not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the instance with the new data from the request
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()

            start_year = serializer.data["fiscal_year_start"]
            scenario_id = serializer.data["scenario_id"]
            print(scenario_id)

            data2 = self.updateSpecialAssessment(scenario_id,start_year)
            return Response({
                'message': 'Data updated successfully',
                'data': serializer.data,
                'data2': data2
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
    def updateSpecialAssessment(self ,scenario_id, fiscal_year_start):
        try:
            start_year_id = SpecialAssessments.objects.filter(scenario_id = scenario_id).order_by("id")[0].id
            start_date = int(fiscal_year_start.split('-')[0])
            for i in range(29):
                date1 = start_date+i
                date2 = date1 + 1
                year_range = str(date1)+"-"+str(date2)
                obj = SpecialAssessments.objects.get(id = start_year_id)
                obj.year = year_range
                obj.save()
                start_year_id += 1
                # new_instance.save()
                serializer3 = self.serializer_class(obj)
            return serializer3.data
        except Exception as e:
            return str(e)
     


##################################################  Units If Variable API's  #################################
class ListUnitsIfVariableAPIView(ListAPIView):
    """This endpoint list all of the available units If Variable from the database"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = UnitsIfVariable.objects.all()
    serializer_class = UnitsIfVariableSerializer

class GetnitsIfVariableAPIView(generics.GenericAPIView):
    """
        Desc: for getting particular record of units If Variable by scenario_id or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnitsIfVariableSerializer
    def get(self, request,id):
        try:
            queryset = UnitsIfVariable.objects.filter(scenario_id=id)
            serializer = self.get_serializer(queryset, many=True)

            return Response({
                'data': serializer.data,
                })
        except Exception as e:
            return Response({'message': str(e)})  


class createORupdateUnitsIfVariableAPIView(generics.GenericAPIView):
    """
    This endpoint allows for creating or updating Components records.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', [])
        created_records = []
        updated_records = []
        
        for record_data in data:
            record_id = record_data.get('id')
            serializer = UnitsIfVariableSerializer(data=record_data)
            if serializer.is_valid():
                if record_id:
                    # Update existing record
                    record = UnitsIfVariable.objects.get(id=record_id)
                    serializer.update(record, serializer.validated_data)
                    updated_records.append(serializer.data)
                else:
                    # Create new record
                    serializer.save()
                    created_records.append(serializer.data)
        
        response_data = {
            'created_records': created_records,
            'updated_records': updated_records
        }
        return Response(response_data, status=status.HTTP_200_OK)


class DeleteUnitsIfVariableAPIView(DestroyAPIView):
    """This endpoint allows for deletion of a specific units if variable from the database"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = UnitsIfVariable.objects.all()
    serializer_class = UnitsIfVariableSerializer


 # ###########################################  SpecialAssessments API  #########################################
class SpecialAssessmentsList(ListAPIView):
    """
    This endpoint list all of the available Special Assessment record from the database
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpecialAssessments.objects.all()
    serializer_class = SpecialAssessmentsSerializer

class GetSpecialAssessments(generics.GenericAPIView):
    """
        Desc: for getting particular record of Special Assessment by scenario_id or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SpecialAssessmentsSerializer
    def get(self, request,id):
        try:
            queryset = SpecialAssessments.objects.filter(scenario_id=id).order_by("id")
            serializer = self.get_serializer(queryset, many=True)
            return Response({
            'data': serializer.data,
            })
        except Exception as e:
            return Response({'message': str(e)})  
    

class SpecialAssessmentsUpdate(generics.GenericAPIView):
    """
    update the multiple Special Assessment record 
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = SpecialAssessments.objects.all()
    serializer_class = SpecialAssessmentsSerializer

    def put(self, request, *args, **kwargs):

        data = request.data.get('data', [])
        queryset = self.filter_queryset(self.get_queryset())

        # update each object in the queryset
        for item in data:
            obj = queryset.get(id=item.get('id'))
            serializer = self.get_serializer(obj, data=item, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response({'status': 'updated'})

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
    

 #############################################################   Component API  #################################
class ComponentsList(ListAPIView):
    """
    This endpoint list all of the available Components List record from the database
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer

class GetComponents(generics.GenericAPIView):
    """
        Desc: for getting particular record by Components List scenario_id or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ComponentsSerializer
    def get(self, request,id):
        try:
            queryset = Components.objects.filter(scenario_id=id).order_by('id')
            serializer = self.get_serializer(queryset, many=True)
            return Response({
            'data': [serializer.data],
            })
        except Exception as e:
            return Response({'message': str(e)})  
        

class ComponentsCreateOrUpdate(generics.GenericAPIView):
    """
    This endpoint allows for creating or updating Components records.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', [])
        created_records = []
        updated_records = []
        
        for record_data in data:
            record_id = record_data.get('id')
            serializer = ComponentsSerializer(data=record_data)
            
            if serializer.is_valid():
                if record_id:
                    # Update existing record
                    try:
                        record = Components.objects.get(id=record_id)
                        serializer.update(record, serializer.validated_data)
                        updated_records.append(serializer.data)
                    except Components.DoesNotExist:
                        pass
                else:
                    # Create new record
                    serializer.save()
                    created_records.append(serializer.data)
        
        response_data = {
            'created_records': created_records,
            'updated_records': updated_records
            
        }
        print(created_records)
        return Response(response_data, status=status.HTTP_200_OK)


##############################################  loan and other expendature  ######################################

class GetLoanOtherExpenditures(generics.GenericAPIView):
    """
        Desc: for getting particular record by LoanOtherExpenditures or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LoanOtherExpendituresSerializer
    def get(self, request,id):
        try:
            queryset = LoanOtherExpenditures.objects.filter(scenario_id=id).order_by('id')
            serializer = self.get_serializer(queryset, many=True)
            return Response({
            'data': serializer.data,
            })
        except Exception as e:
            return Response({'message': str(e)})  


class createORupdateLoanOtherExpenditures(generics.GenericAPIView):
    """
    This endpoint allows for creating or updating LoanOther Expenditures records.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data = request.data.get('data', [])
        created_records = []
        updated_records = []

        for record_data in data:
            record_id = record_data.get('id')
            serializer = LoanOtherExpendituresSerializer(data=record_data)
            
            if serializer.is_valid():
                if record_id:
                    # Update existing record
                    try:
                        record = LoanOtherExpenditures.objects.get(id=record_id)
                        serializer.update(record, serializer.validated_data)
                        updated_records.append(serializer.data)
                    except LoanOtherExpenditures.DoesNotExist:
                        pass
                else:
                    serializer.save()
                    created_records.append(serializer.data)
        
        response_data = {
            'created_records': created_records,
            'updated_records': updated_records
        }
        return Response(response_data, status=status.HTTP_200_OK)
    

   
############################################################## Component download csv #############################
class ComponenetCsv(generics.GenericAPIView):
    serializer_class = ComponenetCsvSwaggerSerializer
    #thats create csv file of components
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request,id):
        response = HttpResponse(content_type='text/csv')
   
        #decide the file name
        response['Content-Disposition'] = 'attachment; filename="components_list.csv"'
        response['filename'] = 'components_list.csv'

        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8'))

        #write the headers
        writer.writerow([
            smart_str(u"Category"),
            smart_str(u"Component_title"),
            smart_str(u"Description"),
            smart_str(u"useful_life_year"),
            smart_str(u"remaining_useful_life_years"),
            smart_str(u"Current_replacement_cost"),
            smart_str(u"Assessement"),
            smart_str(u"Fund_component"),
            smart_str(u"Notes")
        ])

        try:
            Component = Components.objects.filter(scenario_id = id).order_by('id')
        except Components.DoesNotExist:
            return Response({'error': 'Component not found.'}, status=status.HTTP_404_NOT_FOUND)

        #get data from database or from text file....
        Component = Components.objects.filter(scenario_id = id)
        #    events = event_services.get_events_by_year(year) #dummy function to fetch data
        for event in Component:
            writer.writerow([
                smart_str(event.category),
                smart_str(event.Component_title),
                smart_str(event.description),
                smart_str(event.useful_life_year),
                smart_str(event.remaining_useful_life_years),
                smart_str(event.current_replacement_cost),
                smart_str(event.assessement),
                smart_str(event.Fund_component),
                smart_str(event.Notes),
            ])
        return response
    
    
 ################################################   MonthalyCommonExpenses API ##############################
class MonthalyCommonList(ListAPIView):
    """
    This endpoint list all of the available Monthaly Common record from the database
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = MonthalyCommonExpenses.objects.all()
    serializer_class = MonthalyCommonExpensesSerializer

class GetMonthalyCommon(generics.GenericAPIView):
    """
        Desc: for getting particular record of Monthaly Common by scenario_id or foreign key from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MonthalyCommonExpensesSerializer
    def get(self, request,id):
        try:
            queryset = MonthalyCommonExpenses.objects.filter(scenario_id=id).order_by('id')
            serializer = self.get_serializer(queryset, many=True)
            return Response({
            'data': serializer.data,
            })
        except Exception as e:
            return Response({'message': str(e)})  
        

class MonthalyCommonCreateOrUpdate(generics.GenericAPIView):
    """
    This endpoint allows for creating or updating Monthaly Common records.
    """
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):

        data = request.data.get('data', [])
        created_records = []
        updated_records = []
        
        for record_data in data:
            record_id = record_data.get('id')
            serializer = MonthalyCommonExpensesSerializer(data=record_data)
            
            if serializer.is_valid():
                if record_id:
                    # Update existing record
                    try:
                        record = MonthalyCommonExpenses.objects.get(id=record_id)
                        serializer.update(record, serializer.validated_data)
                        updated_records.append(serializer.data)
                    except MonthalyCommonExpenses.DoesNotExist:
                        pass
                else:
                    serializer.save()
                    created_records.append(serializer.data)
        
        response_data = {
            'created_records': created_records,
            'updated_records': updated_records
        }
        return Response(response_data, status=status.HTTP_200_OK)

 
class UnactiveMonthlyExpendeture(generics.GenericAPIView):
    """
        Desc: for monthly expendeture unactive from scenario managment model
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioManagementSerializers 
    def put(self, request, scenario_id):
        try:
            status = request.data['status']
            if(status == True):    
                instance = ScenarioManagement.objects.get(id=scenario_id)
                instance.MonthalyCommonExpenses = False
                instance.save()
                
                serializer = self.serializer_class(instance)
                return Response(serializer.data)
        except ScenarioManagement.DoesNotExist:
            return Response({'message': 'Scenario Management instance does not exist'})
        except Exception as e:
            return Response({'message': str(e)})
        
    def get(self, request, scenario_id):
        try:
            instance = ScenarioManagement.objects.get(id=scenario_id)
            status = instance.MonthalyCommonExpenses
            return Response({'status': bool(status)})
        except ScenarioManagement.DoesNotExist:
            return Response({'message': 'Scenario Management instance does not exist'})
        except Exception as e:
            return Response({'message': str(e)})
        

# class GetAccessUserAPIView(generics.GenericAPIView):
#     """
#     Desc: for updating user for access any resource record 
#     """
#     # permission_classes = [permissions.IsAuthenticated]
#     serializer_class = AccessUserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, *args, **kwargs):
#         # partial = kwargs.pop('partial', False)
#         # instance = self.get_object()
#         # serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         # if serializer.is_valid():
#         #     serializer.save()
#         #     return Response(serializer.data)
#         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
#         instance = AccessUser.objects.get()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         serializer.save()

#         return Response({
#         'message': 'Data updated successfully',
#         'data': serializer.data
#         })
#     # except Exception as e:
#     #     return Response({'message': str(e)})
        

# class ScenarioManagementViewSet(viewsets.ModelViewSet):
#     queryset = ScenarioManagement.objects.all()
#     serializer_class = ScenarioManagementSerializers
#     @action(detail=True, methods=['post'])
#     def grant_read_access(self, request, pk=None):
#         scenario = self.get_object()
#         # granting_user = request.user
#         user_id = request.data.get('user_id')
#         user = CustomUser.objects.get(id=user_id)
#         if user_id != scenario.created_by:
#             raise Exception("Only the scenario creator can grant read access.")
#         scenario.read_access_users.add(user)
#         scenario.save()
#         return Response("Read access granted.")
#     @action(detail=True, methods=['post'])
#     def revoke_read_access(self, request, pk=None):
#         scenario = self.get_object()
#         # revoking_user = request.user
#         user_id = request.data.get('user_id')
#         user = CustomUser.objects.get(id=user_id)
#         if user_id != scenario.created_by:
#             raise Exception("Only the scenario creator can revoke read access.")
#         scenario.read_access_users.remove(user)
#         scenario.save()
#         return Response("Read access revoked.")
#     @action(detail=True, methods=['post'])
#     def grant_write_access(self, request, pk=None):
#         scenario = self.get_object()
#         # granting_user = request.user
#         user_id = request.data.get('user_id')
#         user = CustomUser.objects.get(id=user_id)
#         if user_id != scenario.created_by:
#             raise Exception("Only the scenario creator can grant write access.")
#         scenario.write_access_users.add(user)
#         scenario.save()
#         return Response("Write access granted.")
#     @action(detail=True, methods=['post'])
#     def revoke_write_access(self, request, pk=None):
#         scenario = self.get_object()
#         # revoking_user = request.user
#         user_id = request.data.get('user_id')
#         user = CustomUser.objects.get(id=user_id)
#         if user_id != scenario.created_by:
#             raise Exception("Only the scenario creator can revoke write access.")
#         scenario.write_access_users.remove(user)
#         scenario.save()
#         return Response("Write access revoked.")