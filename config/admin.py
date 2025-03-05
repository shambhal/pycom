from django.contrib import admin

# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    actions=None
    list_display=['cname','cvalue']
    def has_add_permission(self, request):
        return False