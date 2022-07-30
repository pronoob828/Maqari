from django.contrib import admin
from maqari.models import Halaqa, HalaqaType

# Register your models here.

class HalaqaAdmin(admin.ModelAdmin):
    list_display = (
        'halaqa_number',
        'teacher',
        'supervisor',
    )
    search_fields = ('halaqa_number', 'teacher')
    readonly_fields = ()

    filter_horizontal = ('students',)
    list_filter = ('gender', 'supervisor', 'teacher',)
    fieldsets = ()

admin.site.register(Halaqa,HalaqaAdmin)
admin.site.register(HalaqaType)
