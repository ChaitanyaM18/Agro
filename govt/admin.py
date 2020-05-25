from django.contrib import admin
from .models import GovtDetails

class GovtDetailsAdmin(admin.ModelAdmin):
	list_display = ['title','link','description']

admin.site.register(GovtDetails,GovtDetailsAdmin)
