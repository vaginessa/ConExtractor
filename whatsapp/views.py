# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from extractor import main
from django.views import View
from models import Conexe


class Index(View):
    template_name = 'main.html'

    def get(self, request):
        return render(request, 'main.html', {})

    def post(self, request):
        if request.is_ajax():
            html = request.POST.get('htmlcode', '')
            if html:
                contact_list = main(html)
                for i in contact_list:
                    Conexe.objects.create(number=i)
                return JsonResponse({"contacts": "\r\n".join(contact_list), "count": len(contact_list)})
            else:
                return JsonResponse({"error": "extraction failed!"})
        else:
            return JsonResponse({"status": False})
