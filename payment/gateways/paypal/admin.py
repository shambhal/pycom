from django.contrib import admin
from .models import Paypal
# Register your models here.
class PaypalAdmin(admin.ModelAdmin):
    actions=None
    actions_on_top=False
    show_save_and_continue=False
    list_display=['status','sort_order']
    def render_change_form(self, request, context,add,change,form_url,obj) :
        context.merge({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
admin.site.register(Paypal,PaypalAdmin)    