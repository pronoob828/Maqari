from django.contrib import admin
from maqari.models import Halaqa, HalaqaType,Exam,ExamType,Stats,HourlyEnrollment
from account.models import Account
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

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

    list_display_links = ('image_preview','halaqa_number')

    autocomplete_fields = ('teacher','supervisor')
    search_fields = ('halaqa_number', 'teacher__username','teacher__last_name','teacher__email',)
    readonly_fields = ()

    filter_horizontal = ('students',)
    list_filter = ('gender','halaqa_type',)

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

    def get_form(self, request, obj=None,**kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['halaqa_number'].disabled = True
            form.base_fields['gender'].disabled = True
            form.base_fields['halaqa_type'].disabled = True
            form.base_fields['supervisor'].disabled = True
            if not request.user == obj.supervisor:
                form.base_fields['teacher'].disabled = True
                form.base_fields['students'].disabled = True
                if not request.user == obj.teacher:
                    form.base_fields['timings'].disabled = True
                    form.base_fields['halaqa_image_url'].disabled = True

        return form

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
        'id',
        'student',
        'halaqa',
        'exam_type',
        'exam_date',
        'is_completed',
        'total_marks_obtained',
        'examiner1',
        'examiner2',
    )

    list_display_links = ('id','student',)

    fieldsets = (
        ("Teacher's Options",{
            'fields':(
                'student',
                'halaqa',
                ('exam_type','exam_halaqah_type'),
                'exam_timing',
                ('exam_from','exam_till','number_of_juz'),
            )
        }),
        ("Examiner Options",{
            'classes':('collapse',),
            'fields':(
                'is_completed',
                ('exam_date','exam_year'),
                ('examiner1','examiner2'),
                ('total_marks_obtained','hifdh_marks_obtained','tajweed_marks_obtained'),                
                'rating',

            )
        })
        )

    autocomplete_fields = ('student',)
    filter_horizontal = ()
    search_fields = ('examiner1__username','examiner1__last_name','examiner2__username','examiner2__last_name','student__username','student__last_name','exam_date')
    list_filter = ('rating', 'is_completed','exam_type','exam_date','exam_year','number_of_juz')

    def open_exam_types(self,obj):
        open_exam_types = ExamType.objects.filter(is_open=True).all()
        return open_exam_types

    def get_form(self, request, obj=None,**kwargs):
        form = super().get_form(request, obj, **kwargs)

        current_user = request.user
        user_subordinates = current_user.get_subordinates()
        
        form.base_fields['exam_type'].queryset = ExamType.objects.filter(is_open = True).all()
        form.base_fields['examiner1'].queryset = Group.objects.get(name="Examiner").user_set
        form.base_fields['examiner2'].queryset = Group.objects.get(name="Examiner").user_set
        form.base_fields['student'].queryset = Account.objects.filter(id__in = user_subordinates)
        form.base_fields['halaqa'].queryset = Halaqa.objects.filter(teacher = current_user) | Halaqa.objects.filter(supervisor = current_user)

        if not (request.user.is_supervisor or request.user.is_superuser or request.user.is_examiner):
            form.base_fields['exam_date'].disabled = True
            form.base_fields['examiner1'].disabled = True
            form.base_fields['examiner2'].disabled = True
            form.base_fields['rating'].disabled = True
            form.base_fields['total_marks_obtained'].disabled = True
            form.base_fields['hifdh_marks_obtained'].disabled = True
            form.base_fields['tajweed_marks_obtained'].disabled = True
            form.base_fields['is_completed'].disabled = True

        return form

class StatsAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'account',
        'halaqa',
        'attendance',
        'dars',
        'murajia',
    )

    autocomplete_fields = ('account',)
    search_fields = ('account__username','account__last_name','account__email','date','halaqa__halaqa_number')
    list_filter = ('halaqa','date')

    def get_form(self, request, obj=None,**kwargs):
        form = super().get_form(request, obj, **kwargs)

        current_user = request.user
        user_subordinates = current_user.get_subordinates()

        form.base_fields['account'].queryset = Account.objects.filter(id__in = user_subordinates)
        form.base_fields['halaqa'].queryset = Halaqa.objects.filter(teacher = current_user) | Halaqa.objects.filter(supervisor = current_user)


        return form

class HourlyEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment_number',
        'student',
        'total_hours',
        'hours_left',
        'enrollment_type',
    )

    autocomplete_fields = ('student',)
    search_fields= ('student__username','student__last_name','student__email','enrollment_number')
    list_filter = ('total_hours','enrollment_type','hours_left')
    list_editable = ('hours_left',)
    list_display_links = ('student','enrollment_number')

    def get_form(self, request, obj=None,**kwargs):
        form = super().get_form(request, obj,**kwargs)
        is_superuser = request.user.is_superuser
        is_teacher = request.user.is_teacher
        is_supervisor = request.user.is_supervisor
        
        if not (is_supervisor or is_superuser):
            form.base_fields['student'].disabled = True
            form.base_fields['enrollment_number'].disabled = True
            form.base_fields['total_hours'].disabled = True
            form.base_fields['enrollment_type'].disabled = True
            if not is_teacher:
                form.base_fields['hours_left'].disabled= True

        return form

class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('user','content_type','object_id','object_repr','action_flag','change_message')

admin.site.register(Halaqa,HalaqaAdmin)
admin.site.register(HalaqaType)
admin.site.register(Exam,ExamAdmin)
admin.site.register(ExamType,ExamTypeAdmin)
admin.site.register(Stats,StatsAdmin)
admin.site.register(HourlyEnrollment,HourlyEnrollmentAdmin)
admin.site.register(LogEntry,LogEntryAdmin)