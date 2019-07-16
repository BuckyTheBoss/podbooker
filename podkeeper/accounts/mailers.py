from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.conf import settings
from mailjet_rest import Client



def send_confirmation_email(request, user):
  mailjet = Client(
    auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE),
    version='v3.1', 
    api_url='https://api.mailjet.com/'
  )

  current_site = get_current_site(request)
  data = {
    'Messages': [
      {
        "From": {
          "Email": settings.MJ_SENDER_EMAIL,
          "Name": "PodBooker - Signup"
        },
        "To": [
          {
            "Email": user.email,
            "Name": user.first_name
          }
        ],
        "TemplateID": 914859,
        "TemplateLanguage": True,
        "Subject": "PodBooker Email Verification",
        "Variables": {
          "first_name": user.first_name,
          "activation_link": render_to_string('activate_account_email.html', {
          'domain': current_site.domain,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': account_activation_token.make_token(user),
        })
        }
      }
    ]
  }

  mailjet.send.create(data=data)




def reset_password_email(request, user):
  mailjet = Client(
    auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE),
    version='v3.1', 
    api_url='https://api.mailjet.com/'
  )

  current_site = get_current_site(request)
  data = {
    'Messages': [
      {
        "From": {
          "Email": settings.MJ_SENDER_EMAIL,
          "Name": "PodBooker Contact"
        },
        "To": [
          {
            "Email": user.email,
            "Name": user.first_name
          }
        ],
        "TemplateID": 889076,
        "TemplateLanguage": True,
        "Subject": "PodBooker Password Reset",
        "Variables": {
          "first_name": user.first_name,
          "password_reset_link": render_to_string('password_link.html', {
          'domain': current_site.domain,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': account_activation_token.make_token(user),
        })
        }

      }
    ]
  }

  mailjet.send.create(data=data)