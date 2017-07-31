# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from extractor import main
from django.views import View
from validate_email import validate_email
from .forms import DivForm
import requests
import os
import re

try:
    from whatpro.secret import CAPTCHA_KEY, MAILCHIMP_API_KEY, LIST_ID
except ImportError as im:
    SECRET_KEY = os.environ.get('CAPTCHA_KEY', '')
    MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
    LIST_ID = os.environ.get('LIST_ID', '')

MAILCHIMP_URL = 'https://us16.api.mailchimp.com/3.0/lists/2a0abae869/members/'


# Separate saved and not saved contacts
def separeate(contacts):
    saved = list()
    not_saved = list()
    for contact in contacts:
        decision = bool(re.search(r'[a-zA-Z]', contact))
        if decision:
            saved.append(contact)
        else:
            not_saved.append(contact)
    return saved, not_saved


class Index(View):
    template_name = 'form.html'
    form_class = DivForm

    def get(self, request, *args, **kwargs):
        form = DivForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)

            ''' reCAPTCHA validation '''
            recaptcha_response = request.POST.get('recaptcha-response')
            data = {
                'secret': CAPTCHA_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' reCAPTCHA validation ends'''

            if result.get('success', '') and form.is_valid():
                contact_list = main(form.cleaned_data["textarea"])
                saved, notsaved = separeate(contact_list)
                contacts = "You Have {} Saved Contacts\n\n".format(len(saved))
                contacts += "\r\n".join(saved)
                contacts += "\r\n\r\nYou have {} Contacts which are not saved\n\n".format(len(notsaved))
                contacts += "\r\n".join(notsaved)
                return JsonResponse({"contacts": contacts, "count": len(contact_list)})
            else:
                return JsonResponse({"error": "extraction failed!"})
        else:
            return JsonResponse({"status": False})


def newsletter(request):
    if request.is_ajax() and request.method == 'POST':
        email = request.POST.get('email', False)
        if email:
            auth = ('hackprodev', MAILCHIMP_API_KEY)
            headers = {'Content-Type': 'application/json'}
            is_valid = validate_email(email)
            if is_valid:
                data = {
                    'email_address': email,
                    'status': 'subscribed'
                }
                response = requests.post(MAILCHIMP_URL, auth=auth, headers=headers, json=data)
                data = {
                    "status": True if response.status_code == 200 else False
                }
                return JsonResponse(data)
            else:
                return JsonResponse({"status": "SPAM"})
        else:
            HttpResponse('', status=404)
    else:
        return HttpResponse('', status=404)
