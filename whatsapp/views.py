# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from extractor import main
from django.views import View
from .forms import DivForm
import requests
import os
import sys

try:
    from whatpro.secret import CAPTCHA_KEY
except ImportError as im:
    SECRET_KEY = os.environ.get('CAPTCHA_KEY', '')
    if not SECRET_KEY:
        print(im, " and You don't have CAPTCHA_KEY in environment !")
        sys.exit(0)


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
                return JsonResponse({"contacts": "\r\n".join(contact_list), "count": len(contact_list)})
            else:
                return JsonResponse({"error": "extraction failed!"})
        else:
            return JsonResponse({"status": False})