from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('login/', views.LoginAPI.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update/<int:pk>/', views.UserUpdateAPI.as_view(), name='user-update'),
    path('password-reset/<int:pk>/',views.PasswordResetAPI.as_view(),name="password_reset"),
    path("forget-password/",views.ForgetPassword.as_view(),name= "forget_password"),
    path("verify-otp/",views.VerifyOTP.as_view(),name = "verify_otp"),
    path("change-password/",views.ChangePassword.as_view(),name = "change-password"),
    path('user-list/', views.UserList.as_view(), name="user-list"),
    #CommunityInfo API urls
    path('communityInfo-create/', views.CreateCommunityInfoAPIView.as_view(), name='CommunityInfo_create'),
    path('communityInfo-list/', views.ListCommunityInfoAPIView.as_view(), name='CommunityInfo_list'),
    path('communityInfo-update/<int:pk>/', views.UpdateCommunityInfoAPIView.as_view(), name='CommunityInfo_update'),
    path('communityInfo-delete/', views.DeleteCommunityInfoAPIView.as_view(), name='CommunityInfo_delete'),
    path('communityInfo/view/<int:user_id>/', views.AccountsAndCommunityInfoAPIView.as_view(), name='AccountsAndCommunityInfo_view'),
    
]