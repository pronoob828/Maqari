from django.contrib import admin
from maqari.models import Halaqa, HalaqaType
from account.models import Account
from django.contrib.auth.models import Group

# Register your models here.

class TeacherFilter(admin.SimpleListFilter):
    title = 'Teacher'
    parameter_name = 'teacher'
    teacher_ids = []

    def lookups(self, request, model_admin):
        data = []
        for object in Group.objects.get(name = self.title).user_set.all():
            data.append((object.get_full_name(),object.get_full_name()))
            self.teacher_ids.append(object.id)
        return data
    
    def queryset(self, request, queryset):
        return queryset.filter(teacher = Account.objects.get(id__in = self.teacher_ids))      


class HalaqaAdmin(admin.ModelAdmin):
    list_display = (
        'halaqa_number',
        'teacher',
        'supervisor',
    )
    search_fields = ('halaqa_number', 'teacher')
    readonly_fields = ()

    filter_horizontal = ('students',)
    list_filter = ('gender', 'supervisor',TeacherFilter)
    fieldsets = ()

admin.site.register(Halaqa,HalaqaAdmin)
admin.site.register(HalaqaType)
