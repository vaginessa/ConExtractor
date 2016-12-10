from django.contrib import admin
from models import Conexe


# Register your models here.

class ConModelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'number', 'timestamp')

    class Meta:
        models = Conexe


admin.site.register(Conexe, ConModelAdmin)
