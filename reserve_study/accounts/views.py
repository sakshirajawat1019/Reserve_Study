from django.shortcuts import render
from rest_framework import generics, status
from .serializers import UserSerializer, PasswordResetSerializer, CustomUserSerializer, CustomTokenObtainPairSerializer, \
    UpdateSerializer
from rest_framework import permissions
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
# from .formula import generate_password
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import CommunityInfo,CustomUser
from .serializers import CommunityInfoSerializer
import random
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist

class UserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    
    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)

    #     # Create an entry in the community_info model with default values
    #     user = self.request.user

    #     community_info_data = {
    #         'user_id': user.pk,
    #         'community_name': 'Default Community Name',
    #         'community_address': 'demo address',
    #         'subscription_type': 'standard',
    #         'period': '2023-2024',
    #         'max_number_of_scenarios': 5,
    #         'subscription_status': True
    #         # Set other default values for community_info fields here
    #     }
    #     community_info_serializer = CommunityInfoSerializer(data=community_info_data)
    #     if community_info_serializer.is_valid():
    #         ss = community_info_serializer.save()
    #     else:
    #         # Handle serializer errors if necessary
    #         return Response(community_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #     return response


class UserUpdateAPI(generics.UpdateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UpdateSerializer
    

class PasswordResetAPI(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        User = get_user_model()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(pk=self.kwargs['pk'])
            if not user.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    User = get_user_model()
    queryset = User.objects.all()


class ForgetPassword(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            if not email:
                return Response({'error': 'Please provide a valid email'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Please provide a valid email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid email ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(record)
        user_email = serializer.data.get('email')
        number_list = [x for x in range(10)]  # Use of list comprehension
        code_items_for_otp = []

        for _ in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item) for item in code_items_for_otp)  # list comprehension again

        # A six-digit random number from the list will be saved in 'otp' field of the user record
        record.otp = code_string
        record.save()

        email = EmailMessage('Reset Password', f'Your OTP is: {code_string}', to=[user_email])
        email.send()

        return Response({'message': 'An OTP has been sent to your email address.'})
    
class VerifyOTP(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            
            if not email or not otp:
                return Response({'error': 'Please provide a valid email and OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Please provide a valid email and OTP'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid email ID.'}, status=status.HTTP_404_NOT_FOUND)

        if record.otp == otp:
            # OTP matched, you can perform the desired action here, such as resetting the password
            return Response({'message': 'OTP matched. Proceed with password reset.'})
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.hashers import make_password

class ChangePassword(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            new_password = request.data.get('new_password')

            if not email or not new_password:
                return Response({'error': 'Please provide a valid email, OTP, and new password'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error': 'Please provide a valid email, OTP, and new password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            record = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid email ID.'}, status=status.HTTP_404_NOT_FOUND)

        # Change the user's password
        record.password = make_password(new_password)
        record.save()

        return Response({'message': 'Password changed successfully.'})

# CommunityInfo Api's 

class CreateCommunityInfoAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    """This endpoint allows for creation of a specific CommunityInfo from the database"""
    queryset = CommunityInfo.objects.all()
    serializer_class = CommunityInfoSerializer

class ListCommunityInfoAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    """This endpoint list all of the available CommunityInfo from the database"""
    queryset = CommunityInfo.objects.all()
    serializer_class = CommunityInfoSerializer

class UpdateCommunityInfoAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    """This endpoint allows for updating a specific todo by passing in the id of the CommunityInfo to update"""
    queryset = CommunityInfo.objects.all()
    serializer_class = CommunityInfoSerializer

class DeleteCommunityInfoAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    """This endpoint allows for deletion of a specific CommunityInfo from the database"""
    queryset = CommunityInfo.objects.all()
    serializer_class = CommunityInfoSerializer

# fetch data for account and community_info page
class AccountsAndCommunityInfoAPIView(generics.GenericAPIView):
    """This endpoint allows to show account section and cummunity section of a specific CommunityInfo from the database"""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, *args, **kwargs):
        try:
            record = CommunityInfo.objects.get(user_id=user_id)
        except CommunityInfo.DoesNotExist:
            return Response({'error': 'CommunityInfo not found.'}, status=status.HTTP_404_NOT_FOUND)
        cumm_serializer = CommunityInfoSerializer(record)
        community_name = cumm_serializer.data.get('community_name')
        community_address = cumm_serializer.data.get('community_address')
        subscription_type = cumm_serializer.data.get('subscription_type')
        period = cumm_serializer.data.get('period')
        max_number_of_scenarios = cumm_serializer.data.get('max_number_of_scenarios')
        subscription_status = cumm_serializer.data.get('subscription_status')
    
        try:
            user_record = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = CustomUserSerializer(user_record)
        first_name = user_serializer.data.get('first_name')
        last_name = user_serializer.data.get('last_name')
        email = user_serializer.data.get('email')
        phone_no = user_serializer.data.get('phone_no')
        company = user_serializer.data.get('company')
        position = user_serializer.data.get('position')
        additional_info = user_serializer.data.get('additional_info')
        role = user_serializer.data.get('role')
        is_active = user_serializer.data.get('is_active')

        response = {
            'user_Detail': {
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'phone_no':phone_no,
                'company':company,
                'position':position,
                'additional_info':additional_info,
                'role':role,
                'account_status':is_active,
                'connected_community':community_name,
                'registration_date':period,

            },
            'community_info':{

                'community_name':community_name,
                'community_address':community_address,
                'subscription_type':subscription_type,
                'period':period,
                'max_number_of_scenarios':max_number_of_scenarios,
                'subscription_status':subscription_status,

            }
        }


        return Response(response, status=status.HTTP_200_OK)
