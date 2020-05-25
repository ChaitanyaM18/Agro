from django.contrib import admin
from .models import States,StateCrops

class StatesAdmin(admin.ModelAdmin):
	list_display = ['state_name','state_image']

class StateCropsAdmin(admin.ModelAdmin):
	list_display = ['state','crop_image','crop_description','fertilizers']

admin.site.register(States,StatesAdmin)
admin.site.register(StateCrops,StateCropsAdmin)
