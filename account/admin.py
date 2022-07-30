from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from account.models import Account,Role

# Register your models here.
admin.site.site_header = "Idarah Al-Maqari' Al-Madinah"
admin.site.index_title = "Admin"
admin.site.site_title = "Maqari' Al-Madinah"

class AccountAdmin(UserAdmin):

    list_display = (
        "username",
        "last_name",
        "email",
        "group_list",
        "in_halaqa",
    )
    list_editable = ()
    list_display_links=("username","last_name","email")

    search_fields = ('email','username','last_name','phone_num','nationality','current_residence','students_halaqa__halaqa_number','teacher_in_halaqaat__halaqa_number')
    readonly_fields = ('date_joined','last_login','in_halaqa')

    filter_horizontal = ('groups','user_permissions')
    list_filter = ('date_joined','groups','is_staff','is_superuser','gender','students_halaqa__halaqa_number')
    fieldsets = ()

    def in_halaqa(self, obj):
        return list(set([halaqa.halaqa_number for halaqa in obj.students_halaqa.all()] + [halaqa.halaqa_number for halaqa in obj.teacher_in_halaqaat.all()]))

    def group_list(self,obj):
        return [group.name for group in obj.groups.all()]


admin.site.register(Role)
admin.site.register(Account, AccountAdmin)

