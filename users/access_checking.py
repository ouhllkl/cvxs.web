from django.shortcuts import render, redirect
from .models import *

def check_access_type_1(request): # login and cvx acceptance

    r_data = {'status': True}

    if not request.user.is_anonymous:
        if request.user.profile.cvx_acceptance != 1:
            r_data['status'] = False

            if request.user.profile.cvx_acceptance == 0:
                r_data['message_title'] = "You havn't been accepted in cvx student program"
                r_data['message_detail'] = 'please wait untill we review your applicaiton'

            elif request.user.profile.cvx_acceptance == -1:
                r_data['message_title'] = "you are not accepted as a student in cvx students program"
                r_data['message_detail'] = "you can't access this page if you haven't been accepted in cvx students program"
        
        
    else:
        r_data['status'] = False
        r_data['message_title'] = "You aren't signed in"
        r_data['message_detail'] = 'please sign in to access this page'
        

    return r_data




def check_access_type_2(request, access_type): # administration check 
    
    r_data = check_access_type_1(request)

    if r_data['status']:
        if bool(len(administration_profile.objects.filter(user = request.user))):
            if not getattr(administration_profile.objects.filter(user = request.user)[0], access_type):
                r_data['status'] = False
                r_data['message_title'] = "Access Denied"
                r_data['message_detail'] = "You don't have the permission to open this page"

        else:
            r_data['status'] = False
            r_data['message_title'] = "Access Denied"
            r_data['message_detail'] = "You don't have the permission to open this page"


    return r_data