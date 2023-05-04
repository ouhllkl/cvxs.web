"""cvx_students URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('profile/<int:user_id>/', profile, name='profile'),
    path('login/',                 login_page, name= 'login'),
    path('create/',                 create_user, name= 'create_user_account'),
    path('profile/',                 edit_profile, name= 'edit_profile'),


    

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_cmplete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('activate_request/', activate_request, name='activate_request'),
    path('activate_request_sended/', activate_request_sended, name='activate_request_sended'),
    
    path('applications_requests/', applications_requests, name='applications_requests'),
    
    path('procedure/<int:procedure_id>/', view_procedure, name='view_procedure'),
    path('procedures/', view_procedures, name='view_procedures'),
    path('step/<int:step_id>/', view_step, name='view_step'),

    

    path('activate/<uidb64>/<token>', activate, name='activate'),

    
    path('support_groups/', view_support_groups, name='view_support_groups'),
    path('support_group/<int:group_id>/', view_support_group, name='view_support_group'),
    path('join_requests/<int:group_id>/', view_join_requests, name='view_join_requests'),
    path('help_requests/<int:group_id>/', view_help_requests, name='view_help_requests'),


    
    




]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

