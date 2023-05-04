from django.shortcuts import render, redirect
from .access_checking import *
from .models import *
from .forms import *
from .notifications_center import *
from django.contrib.auth import  login, authenticate
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token
from django.contrib import messages


def profile(request, user_id):
    user_obj = User.objects.get(id = user_id)

    if user_obj.profile.current_procedure != None:
        user_procedure_steps = user_obj.profile.current_procedure.procedurestep_set.all().order_by('level')
        


    else:
        user_procedure_steps = None
    
    
    if request.method == 'POST':
        
        if 'accept' in request.POST:
            user_obj.profile.cvx_acceptance = 1
            notify_user(request, user_obj, 'CVX Application Status Update', html_template='application_status', html_kwargs={'user_t': user_obj, 'status': 'Accepted'})

        if 'declines' in request.POST:
            user_obj.profile.cvx_acceptance = -1
            notify_user(request, user_obj, 'CVX Application Status Update', html_template='application_status', html_kwargs={'user_t': user_obj, 'status': 'Denied'})

        if 'reviewing' in request.POST:
            user_obj.profile.cvx_acceptance = 0            
            notify_user(request, user_obj, 'CVX Application Status Update', html_template='application_status', html_kwargs={'user_t': user_obj, 'status': 'Under review'})
        
        

        if 'change_procedures' in request.POST:
            procedure_form = user_procedures_form(request.POST, instance= User.objects.get(pk = user_id).profile )
            if procedure_form.is_valid():
                procedure_form.save()
                
     
            current_procedure = procedure_form.cleaned_data['current_procedure']
            user_obj.profile.current_procedure = current_procedure
            user_obj.profile.current_procedure_completed = False
            user_obj.profile.save()


            
            notify_user(request, user_obj, 'Update on Your Current Procedure in CVX Platform', html_template='Procedure_changed', html_kwargs={'user_t': user_obj, 'procedure': current_procedure})


        if 'start_procedure' in request.POST:
            user_obj.profile.current_procedure_step = ProcedureStep.objects.get(pk = int(request.POST.get('current_procedure_step')))
            user_obj.profile.save()
        
        if 'complete_step' in request.POST:
            print((request.POST))
            print(list(user_procedure_steps))

            current_steo_index = list(user_procedure_steps).index(ProcedureStep.objects.get(pk = int(request.POST.get('current_step'))))
            print(current_steo_index, len(user_procedure_steps))
            if current_steo_index < len(user_procedure_steps)-1:
                user_obj.profile.current_procedure_step = user_procedure_steps[current_steo_index+1]
                user_obj.profile.save()

            else:
                user_obj.profile.current_procedure_step = None
                user_obj.profile.current_procedure_completed = True
                user_obj.profile.save()



        user_obj.profile.save()

    procedures_form = user_procedures_form(instance= User.objects.get(pk = user_id).profile )

    cvx_acceptance_handler = False
    change_procedures_handler = False

    administration_request = len(administration_profile.objects.filter(user = request.user))
    if administration_request:
        cvx_acceptance_handler = administration_profile.objects.filter(user = request.user)[0].cvx_acceptance_handler
        change_procedures_handler =  administration_profile.objects.filter(user = request.user)[0].change_current_procedures

    if user_obj.profile.current_procedure != None:
        
        
        status = 1
        if user_obj.profile.current_procedure_step != None:
            print(1)
            for step in user_procedure_steps:
                
                print(type(step), type(user_obj.profile.current_procedure_step.step))
                if step == user_obj.profile.current_procedure_step:
                    print(2)
                    status = -1
                    step.c_status = 0 

                else:
                    print(3)
                    step.c_status = status
        else:
            for step in user_procedure_steps:
                step.c_status = -1
    

    else:
        user_procedure_steps = None
    

        
    
    data = {
        'user_obj': user_obj,
        'administration_request': len(administration_profile.objects.filter(user = request.user)),
        'cvx_acceptance_handler': cvx_acceptance_handler,
        'change_procedures_handler':change_procedures_handler,
        'procedures_form': procedures_form,
        'user_procedure_steps':user_procedure_steps,
    }


    return render(request, 'profile.html', data)






def view_support_groups(request):
    check_1 = check_access_type_1(request)
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    
    data = {
        'groups': SupportGourp.objects.all()
    }

    return render(request, 'support_groups.html', data)




def view_support_group(request, group_id):

    check_1 = check_access_type_1(request)
    if not check_1['status']:
        return render(request, 'access_denied.html', check_1)
    
    group = SupportGourp.objects.get(pk = group_id)

    if request.method == 'POST':
        
        if 'SupportGroupHelpRequest' in request.POST:
            support_group_help_request                  =  SupportGroupHelpRequest_form(request.POST, initial={"user": request.user.pk, 'support_gourp' : group_id})

            if support_group_help_request.is_valid():
                support_group_help_request.save()

                notify_user(request, group.admin, 'Help request 1', html_template='help_request', html_kwargs={'user_t': group.admin, 'group': group})
                
                for member in SupportGourpUser.objects.filter(support_gourp = group):
                    
                    notify_user(request, member.user, 'Help request 2', html_template='help_request', html_kwargs={'user_t':member.user, 'group': group})
            
            else:
                print(support_group_help_request.errors)

        if 'SupportGroupJoinRequest' in request.POST:
            support_group_join_request                  =  SupportGroupJoinRequest_form(request.POST, initial={"user": request.user.pk, 'support_gourp' : group_id})

            if support_group_join_request.is_valid():
                support_group_join_request.save()
                notify_user(request, group.admin, 'Join request', html_template='join_request', html_kwargs={'user_t': group.admin, 'group': group})
                
            
            else:
                print(support_group_join_request.errors)

    

    SupportGroupHelpRequestForm = SupportGroupHelpRequest_form(initial={"user": request.user.pk, 'support_gourp' : group_id})
    SupportGroupJoinRequestForm = SupportGroupJoinRequest_form(initial={"user": request.user.pk, 'support_gourp' : group_id})

    join_requests_count = SupportGroupJoinRequest.objects.filter(support_gourp = group).count()
    help_requests_count = SupportGroupHelpRequest.objects.filter(support_gourp = group).count()


    
    user_in_group = request.user in [a.user for a in group.supportgourpuser_set.all()]


    return render(request, 'support_group.html', {'group': group, 'SupportGroupHelpRequest': SupportGroupHelpRequestForm, 'SupportGroupJoinRequest':SupportGroupJoinRequestForm, 'join_requests_count':join_requests_count, 'group_id': group_id, 'user_in_group': user_in_group, 'help_requests_count':help_requests_count})


def view_join_requests(request, group_id):
    group = SupportGourp.objects.get(pk = group_id)

    if group.admin != request.user :
        return render(request, 'access_denied.html', {'message_title':'Access Denied', 'message_detail': "you can't view this page, because you are not the admin of this group"})
    
    
    if request.method == 'POST':
        join_request = SupportGroupJoinRequest.objects.get(pk = int(request.POST.get('request')[0]))
        user = join_request.user
        if 'accept' in request.POST:
            SupportGourpUser(support_gourp = group, user = user).save()
            join_request.delete()
            notify_user(request, user, 'Join request', html_template='join_request_status', html_kwargs={'user_t':user, 'group': group, 'status': 'aproved'})
            
        
        if 'cancel' in request.POST:
            join_request.delete()
            notify_user(request, user, 'Join request', html_template='join_request_status', html_kwargs={'user_t':user, 'group': group, 'status': 'canceled'})
            


    requests = SupportGroupJoinRequest.objects.filter(support_gourp = group)
    return render(request, 'join_requests.html', {'group': group, 'requests': requests, 'group_id': group_id})



def view_help_requests(request, group_id):
    group = SupportGourp.objects.get(pk = group_id)

    if group.admin != request.user and not len(SupportGourpUser.objects.filter(user = request.user)) :
        return render(request, 'access_denied.html', {'message_title':'Access Denied', 'message_detail': "you can't view this page, because you are not the admin of this group"})
    
    
    if request.method == 'POST':
        join_request = SupportGroupHelpRequest.objects.get(pk = int(request.POST.get('i_will_help')))
        user = join_request.user
        

        if 'delete' in request.POST:
            join_request.delete()
        
        elif 'i_will_help' in request.POST:
            join_request.helper = request.user
            join_request.save()
            notify_user(request, join_request.user, 'Help Request', html_template = 'one_will_help_1', html_kwargs = {'from': request.user, 'to': join_request.user, })


    requests = SupportGroupHelpRequest.objects.filter(support_gourp = group)
    return render(request, 'help_requests.html', {'group': group, 'requests': requests, 'group_id': group_id})




def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # check if active
            if User.objects.get(username = form.cleaned_data['username']) != None:
                user = User.objects.get(username = form.cleaned_data['username'])

                if not user.is_active:
                    activateEmail(request, user, user.email)
                    return redirect('activate_request_sended')

            
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            print(user,'user')
            
            if user != None:
                login(request, user)
                return redirect('home')
                
            else:
                try:
                    username_from_email = User.objects.get(email = form.cleaned_data['username'])
                    
                    user = authenticate(
                        username = username_from_email,
                        password = form.cleaned_data['password'],
                    )
                except:
                    pass

                if user is not None:
                    login(request, user)
                    return redirect('home')

                else:
                    form.errors['__all__'] = {'Login failed!': 'Login failed!'}

    return render(request, 'login.html', {'form': form})



def create_user(request):
    form = UserForm(initial={"first_name": '', 'last_name' : '', 'email': '','username':''})
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            user =form.save()
            user.is_active = False
            user.save()
            login(request, user)
            activateEmail(request, user, user.email)
            return redirect('activate_request_sended')
        
        else:
            
            
            messages = form.errors['__all__'].data[0].messages[0]
            return render(request, 'createUser.html', {'form': form, 'messages': messages } )

    else:
        return render(request, 'createUser.html', {'form': form, })


def activate_request_sended(request):
    return render(request, 'activate_request_sended.html')

def activate_request(request):
    activateEmail(request, request.user, request.user.email)

    return redirect('profile', user_id = request.user.pk)

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def edit_profile(request):
    if request.user.is_anonymous:
        return redirect('home')
    
    profile_form = Profile_form(instance=Profile.objects.get(user = request.user))

    profile_p = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        profile_p = Profile.objects.get(user = request.user)
        profile_form = Profile_form(request.POST or None, instance=profile_p)
        if profile_form.is_valid():
            profile_form.save()
            profile_p.save()
            for a_user in administration_profile.objects.filter(notify_for_new_applications = True):
                notify_user(request, a_user.user, 'New application', html_template='new_application', html_kwargs={'user_t': a_user.user})
                
            
            messages.success(request, 'we have recived your application.')
            return redirect('profile', request.user.pk)


    return render(request, 'edit_profile.html', {'form': profile_form,'profile': profile_p })


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('edit_profile')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('homepage')

def applications_requests(request):
    if len(administration_profile.objects.filter(user=request.user)) > 0:
        applications = Profile.objects.filter(cvx_acceptance = 0)
        return render(request, 'applications_requests.html', {'applications': applications})
    
    else:
        return render(request, 'access_denied.html', {'message_title':'Access Denied', 'message_detail': "you can't view this page, because you are not in the cvx administration"})
    


def view_procedure(request, procedure_id):

    procedure = Procedure.objects.get(pk = procedure_id)
    procedure_steps = procedure.procedurestep_set.all().order_by('level')

    return render(request, 'procedure.html',{'procedure':procedure, 'procedure_steps': procedure_steps})


def view_procedures(request):

    procedures = Procedure.objects.all()
    

    return render(request, 'procedures.html',{'procedures':procedures})



def view_step(request, step_id):

    step = StudentStep.objects.get(pk = step_id)
    
    return render(request, 'step.html',{'step':step})



def adminstration_dashboard(request):
    if not len(administration_profile.objects.filter(user = request.user)):
        return render(request, 'access_denied.html', {'message_title':'Access Denied', 'message_detail': "you can't view this page, because you are not in the cvx administration"})

    return render(request, 'adminstration_dashboard.html')

