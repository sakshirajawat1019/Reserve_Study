# apps/management/api/serializers.py

from rest_framework import serializers
# from django.contrib.auth import get_user_model,authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ScenarioManagement,IntialParameters, UnitsIfVariable, SpecialAssessments, Components
from .models import  SpecialAssessments, Components, LoanOtherExpenditures, MonthalyCommonExpenses
class ScenarioManagementSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScenarioManagement
        fields = (
            "id",
            "scenario_name",
            "notes",
            "last_saved_date",
            "last_saved_by",
            "status",
            "active",
            "MonthalyCommonExpenses",
        )
# User = get_user_model()
# class UserSerializers(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = (
#             "email",
#             "first_name",
#             "last_name",
#             "password",
#             "is_active",
#             "is_superuser",
#             "username"
#         )

class IntialParemetersSerializers(serializers.ModelSerializer):
    class Meta:
        model = IntialParameters
        fields = "__all__"

class UnitsIfVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitsIfVariable
        fields = "__all__"

class SpecialAssessmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialAssessments
        fields =(
    "id",
    "scenario_id",
    "year",
    "amount" ,
    "purpose" )

class ComponentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Components
        fields = "__all__"        

class LoanOtherExpendituresSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOtherExpenditures
        fields = "__all__" 

class MonthalyCommonExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthalyCommonExpenses
        fields = "__all__"     

class CurrentFundingPlanSerializer(serializers.Serializer):
    pass

class ComponenetCsvSwaggerSerializer(serializers.Serializer):
    pass


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         if email and password:
#             user = authenticate(email=email, password=password)
#             if user:
#                 if not user.is_active:
#                     raise serializers.ValidationError('User account is disabled.')
#                 refresh = self.get_token(user)
#                 data = {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }
#                 return data
#             else:
#                 raise serializers.ValidationError('Unable to log in with provided credentials.')
#         else:
#             raise serializers.ValidationError('Must include "email" and "password".')            