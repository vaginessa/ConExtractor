# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from extractor import main
from django.views import View
from .forms import DivForm
import time


class Index(View):
    template_name = 'form.html'
    form_class = DivForm

    def get(self, request, *args, **kwargs):
        form = DivForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = self.form_class(request.POST)
            if form.is_valid():
                contact_list = main(form.cleaned_data["textarea"])
                return JsonResponse({"contacts": "\r\n".join(contact_list), "count": len(contact_list)})
            else:
                return JsonResponse({"error": "extraction failed!"})
        else:
            return JsonResponse({"status": False})