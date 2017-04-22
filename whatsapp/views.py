# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from extractor import main
from django.views import View
from .forms import DivForm
from pprint import  pprint as pp
import requests
import os
import sys
import re

try:
    from whatpro.secret import CAPTCHA_KEY
except ImportError as im:
    SECRET_KEY = os.environ.get('CAPTCHA_KEY', '')
    if not SECRET_KEY:
        print(im, " and You don't have CAPTCHA_KEY in environment !")
        sys.exit(0)


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
        pp(request.META)
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
