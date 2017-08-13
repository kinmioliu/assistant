from django.contrib import admin
from base_assistant.models import VersionInfo, Solution, ResponsibilityField, MMLCmdInfo

class VerinfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'platform_ver', 'product_ver', 'verinfo')

class SolutionAdmin(admin.ModelAdmin):
    list_display = ('solutionname', 'url')

class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'introduce', 'plname')

class MMLAdmin(admin.ModelAdmin):
    list_display = ('cmdname', 'responsefield')

list_filter = ('user',)
ordering = ('-created_date',)
search_fields = ('text',)

# Register your models here.
admin.site.register(VersionInfo, VerinfoAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(ResponsibilityField, ResponsibilityAdmin)
admin.site.register(MMLCmdInfo, MMLAdmin)