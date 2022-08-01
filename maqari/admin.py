from django.contrib import admin
from maqari.models import Halaqa, HalaqaType,Exam,ExamType
from account.models import Account
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType

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
        return queryset.filter(teacher__in = Account.objects.filter(id__in = set(self.teacher_ids))) 

class SupervisorFilter(admin.SimpleListFilter):
    title = 'Supervisor'
    parameter_name = 'Supervisor'
    supervisor_ids = []

    def lookups(self, request, model_admin):
        data = []
        for object in Group.objects.get(name = self.title).user_set.all():
            data.append((object.get_full_name(),object.get_full_name()))
            self.supervisor_ids.append(object.id)
        return data
    
    def queryset(self, request, queryset):
        return queryset.filter(teacher__in = Account.objects.filter(id__in = set(self.supervisor_ids)))     

class HalaqaAdmin(admin.ModelAdmin):
    fields = (('halaqa_number','gender','halaqa_type'),'timings',('teacher','supervisor'),'students','halaqa_image_url')

    list_display = (
        'image_preview',
        'halaqa_number',
        'halaqa_type',
        'teacher',
        'view_students_link',
    )

    autocomplete_fields = ('teacher',)
    search_fields = ('halaqa_number', 'teacher',)
    readonly_fields = ()

    filter_horizontal = ('students',)
    list_filter = ('gender','halaqa_type',SupervisorFilter,TeacherFilter)

    def image_preview(self,obj):
        return format_html(f"<img src = {obj.halaqa_image_url} width='35px'>")

    def view_students_link(self, obj):
        count = obj.students.count()
        url = (
            reverse("admin:account_account_changelist")
            + "?"
            + urlencode({"students_halaqa__halaqa_number": f"{obj.halaqa_number}"})
        )
        return format_html('<a href="{}">{} Students</a>', url, count)

    view_students_link.short_description = "Students"

#    def get_form(self, request, obj=None,**kwargs):
 #       form = super().get_form(request, obj, **kwargs)
  #      
   #     form.base_fields['supervisor'].queryset = Group.objects.get(name= "Supervisor").user_set       
#
 #       return form

class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name','is_open','open_status')
    list_editable=('is_open',)
    list_filter = ('is_open',)
    search_fields=('type_name',)
    
    def open_status(self,obj):
        return obj.is_open
    
    open_status.boolean = True

class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'exam_type',
        'exam_date',
        'is_completed',
        'total_marks_obtained',
        'examiner1',
        'examiner2',
    )

    autocomplete_fields = ('student',)
    filter_horizontal = ()
    search_fields = ('examiner1__username','examiner1__last_name','examiner2__username','examiner2__last_name','student__username','student__last_name',)
    list_filter = ('rating', 'is_completed','exam_type','exam_date','exam_year')

    def open_exam_types(self,obj):
        open_exam_types = ExamType.objects.filter(is_open=True).all()
        return open_exam_types

#    def get_form(self, request, obj=None,**kwargs):
 #       form = super().get_form(request, obj, **kwargs)
  #      
   #     form.base_fields['exam_type'].queryset = ExamType.objects.filter(is_open = True)
    #    form.base_fields['examiner1'].queryset = Group.objects.get(name="Examiner").user_set
     #   form.base_fields['examiner2'].queryset = Group.objects.get(name="Examiner").user_set       
#
 #       return form

admin.site.register(Halaqa,HalaqaAdmin)
admin.site.register(HalaqaType)
admin.site.register(Exam,ExamAdmin)
admin.site.register(ExamType,ExamTypeAdmin)
