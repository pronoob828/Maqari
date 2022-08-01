from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.models import Group

# Register your models here.
admin.site.site_header = "Idarah Al-Maqari' Al-Madinah"
admin.site.index_title = "Admin"
admin.site.site_title = "Maqari' Al-Madinah"

class AccountAdmin(UserAdmin):
    list_display = (
        "image_preview",
        "full_name",
        "email",
        "group_list",
        "student_in",
        "teacher_in",
        "supervisor_for"
    )

    fieldsets = (
        ('Main',
            {'fields' : 
                (
                    ('username','last_name'),
                    'email','gender',
                    'phone_num',
                    ('current_residence','nationality'),
                    ('date_joined','last_login'),
                    ('student_in','teacher_in','supervisor_for')
                )
            }
        ),
        ('Teacher Options',
            {'fields': 
                (   
                    'years_of_experience',
                    'qualifications',
                    'profile_image',
                )
            }
        ),
        ('Advanced',
            {   'classes':('collapse',),
                'fields':
                (
                    ('is_active','is_staff','is_admin','is_superuser'),
                    'groups',
                    'user_permissions'
                )
            }
        )
    )
    
    list_editable = ()

    list_display_links = (
        "image_preview",
        "full_name",
        "email"
        )
        
    search_fields = (
        'email',
        'username',
        'last_name',
        'phone_num',
        'nationality',
        'current_residence',
        'students_halaqa__halaqa_number',
        'teacher_in_halaqaat__halaqa_number',
        )

    readonly_fields = ('date_joined','last_login','student_in','teacher_in','supervisor_for')
    
    filter_horizontal = (
        'groups',
        'user_permissions',
        )

    list_filter = (
        'date_joined',
        'groups',
        'is_staff',
        'is_superuser',
        'gender',
        'students_halaqa__halaqa_number',
    )


    def full_name(self,obj):
        return obj.get_full_name()

    def student_in(self, obj):
        halaqas = obj.students_halaqa.all()
        urls = []
        for halaqa in halaqas:
            urls.append(
                reverse("admin:maqari_halaqa_change",args=(halaqa.id,))
            )
        
        display_string = ''

        for halaqa in halaqas:
            i = 0
            display_string += f"<a href='{urls[i]}'>{halaqa.halaqa_number} , </a>"
            i += 1

        return format_html(display_string)

    def teacher_in(self, obj): 
        halaqas = obj.teacher_in_halaqaat.all()
        urls = []
        for halaqa in halaqas:
            urls.append(
                reverse("admin:maqari_halaqa_change",args=(halaqa.id,))
            )
        
        display_string = ''

        for halaqa in halaqas:
            i = 0
            display_string += f"<a href='{urls[i]}'>{halaqa.halaqa_number} , </a>"
            i += 1

        return format_html(display_string)
    
    def supervisor_for(self, obj):
        halaqas = obj.supervised_halaqaat.all()
        urls = []
        for halaqa in halaqas:
            urls.append(
                reverse("admin:maqari_halaqa_change",args=(halaqa.id,))
            )
        
        display_string = ''

        for halaqa in halaqas:
            i = 0
            display_string += f"<a href='{urls[i]}'>{halaqa.halaqa_number} , </a>"
            i += 1

        return format_html(display_string)

    def group_list(self,obj):
        return [group.name for group in obj.groups.all()]

    def image_preview(self,obj):
        return format_html(f"<img src = {obj.profile_image} width='35px'>")

    
#    def get_form(self, request, obj=None,**kwargs):
 #       form = super().get_form(request, obj,**kwargs)
  #      is_superuser = request.user.is_superuser
#
 #       form.base_fields['supervisor'].queryset = Group.objects.filter(name = 'Supervisor').user_set
#
 #       if not is_superuser:
  #          form.base_fields['is_superuser'].disabled = True
   #         form.base_fields["user_permissions"].disabled = True
    #        form.base_fields["groups"].disabled = True
     #   return form

admin.site.register(Account, AccountAdmin)

