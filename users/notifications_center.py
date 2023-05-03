
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
import os
from .tokens import account_activation_token
from django.contrib import messages


def notify_user(request, user, title, message = '', redirect_link = '', html_template = '', html_kwargs = {}):

    
    mail_subject = title
    message = render_to_string( os.path.join('emails', html_template+'.html'), {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }|html_kwargs )
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()