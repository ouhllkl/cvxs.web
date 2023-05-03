
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
import os
from .tokens import account_activation_token
from django.contrib import messages
from django.utils.html import strip_tags


def notify_user(request, user, title, message = '', redirect_link = '', html_template = '', html_kwargs = {}):

    html = render_to_string( os.path.join('emails', html_template+'.html'), {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    }.update(html_kwargs))


    text_content = strip_tags(html)


    email_subject = title
    email_body = text_content
    email_message = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
    

    # Add the HTML content to the email message
    email_message.content_subtype = 'html'
    email_message.attach_alternative(html, 'text/html')

    # Get the text content of the HTML email for email clients that don't support HTML

    email_message.send()