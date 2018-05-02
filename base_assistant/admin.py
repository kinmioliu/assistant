from django.contrib import admin
from base_assistant.models import VersionInfo, Solution, ResponsibilityField, MMLCmdInfo, HashTag, OuterLink, FileInfo, ResoureInfoInt, ResourceInfoStr, ResourceInfoRud, WikiInfo

class VerinfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'platform_ver', 'product_ver', 'verinfo')

class SolutionAdmin(admin.ModelAdmin):
    list_display = ('solutionname', 'url')

class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'introduce', 'plname')

class MMLAdmin(admin.ModelAdmin):
    list_display = ('cmdname', 'responsefield')

class HashTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class OutLinkAdmin(admin.ModelAdmin):
    list_display = ('link_title', 'introduce')

class WikiInfoAdmin(admin.ModelAdmin):
    list_display = ('link', 'title', 'abstract', 'group', 'feature', 'classes')

class FileInfoAdmin(admin.ModelAdmin):
    list_display = ("filename", "introduce", "path", "responsefield")

class ResourceInfoStrAdmin(admin.ModelAdmin):
    list_display = ("file", "line", "name", "code", "cmd_mark", "value")

class ResourceInfoIntAdmin(admin.ModelAdmin):
    list_display = ("file", "line", "name", "code", "cmd_mark", "value")

class ResourceInfoRudAdmin(admin.ModelAdmin):
    list_display = ("file", "line", "name", "code", "cmd_mark", "value", "domain")


# Register your models here.
admin.site.register(VersionInfo, VerinfoAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(ResponsibilityField, ResponsibilityAdmin)
admin.site.register(MMLCmdInfo, MMLAdmin)
admin.site.register(HashTag, HashTagAdmin)
admin.site.register(OuterLink, OutLinkAdmin)
admin.site.register(FileInfo, FileInfoAdmin)
admin.site.register(ResourceInfoStr, ResourceInfoStrAdmin)
admin.site.register(ResoureInfoInt, ResourceInfoIntAdmin)
admin.site.register(ResourceInfoRud, ResourceInfoRudAdmin)
admin.site.register(WikiInfo, WikiInfoAdmin)