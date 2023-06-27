"""
URL configuration for reserve_study project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path


# drf_yasg code starts here
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Reserve Study API",
        default_version='v1',
        description="Welcome to the collection of Reserve_study API's",
        terms_of_service="",
        contact=openapi.Contact(email="sakshirgeitpl@gmail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [

    # path('api-schema',get_schema_view(title = 'api_schema',description='reserve_study_apis'),name='api_schema'),
    path('admin/', admin.site.urls),
    path('scenario-management/',include('scenario_management.urls')),
    path('funding-plan/',include('funding_plan.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('accounts/',include('accounts.urls')),
    path('component-detail/',include('component_detail.urls')),
    path('expenditures/',include('expenditures.urls')),
    path('reports/',include('reports.urls'))
    
]

urlpatterns += [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
