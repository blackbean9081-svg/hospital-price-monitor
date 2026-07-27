from django.contrib import admin

from .models import Hospital, TreatmentPrice

admin.site.register(Hospital)
admin.site.register(TreatmentPrice)
