from typing import Any
from django.contrib import admin
from .models import COD
# Register your models here.

class CODAdmin(admin.ModelAdmin):
    actions=None
    list_display=['status','sort_order']
    def render_change_form(self, request, context,add,change,form_url,obj) -> Any:
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
admin.site.register(COD,CODAdmin)    