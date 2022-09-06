import email
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.template.loader import render_to_string


def send_verifying_email(request, user):
    current_site = get_current_site(request)
    context = {
        'protocol': 'http',
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    message = render_to_string(
        'userapp/verify_email.html',
        context=context
    )
    email = EmailMessage('Verification email', message, to=[user.email],)
    email.send()
