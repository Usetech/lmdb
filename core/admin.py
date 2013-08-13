# coding=utf-8
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from core.models import LegalEntity, AddressObject, AddressObjectType, HeadSpeciality, AddressObjectService, BaseModel

__author__ = 'sergio'


class BaseModelAdmin(admin.ModelAdmin):
    model = BaseModel
    base_fields = ("created_at", "modified_at", "deleted_at")
    list_filter = base_fields
    list_display = base_fields
    fieldsets = (
        (u'Создание/изменение/удаление', {
            'fields': (base_fields,),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'modified_at', 'deleted_at')


class AddressObjectInline(admin.StackedInline):
    model = AddressObject
    classes = ('open',)
    inline_classes = ('open',)
    readonly_fields = BaseModelAdmin.readonly_fields
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ("type", "name", "short_name"),
                    ("full_name", ),
                    ("chief", "chief_sex", "chief_speciality",),
                    ("services",),
                    ("okrug", "address")
                )
            }
        ),
    )
    filter_horizontal = ["services"]

    extra = 0


class LegalEntityAdmin(GuardedModelAdmin, BaseModelAdmin):
    model = LegalEntity
    date_hierarchy = "created_at"
    list_display = ("name", "chief_name", "jur_address",)+BaseModelAdmin.list_display
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ("name",),
                    ("ogrn_code", "inn_code"),
                    ("chief_name",),
                    ("jur_address",),
                    ("fact_address",),
                    ("head_physician",),
                    ("reception_phone", "registry_phone"),
                    ("worktime",)
                )
            }
        ),
    )

    inlines = [AddressObjectInline]


class NamedModelAdmin(BaseModelAdmin):
    date_hierarchy = "created_at"
    search_fields = ("name", )
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры", {
                'fields': ("name",)
            }
        ),
    )
    list_display = ("name", ) + BaseModelAdmin.list_display

class AddressObjectTypeAdmin(NamedModelAdmin):
    model = AddressObjectType


class HeadSpecialityAdmin(NamedModelAdmin):
    model = HeadSpeciality


class AddressObjectServiceAdmin(NamedModelAdmin):
    model = AddressObjectService


admin.site.register(LegalEntity, LegalEntityAdmin)
admin.site.register(AddressObjectType, AddressObjectTypeAdmin)
admin.site.register(HeadSpeciality, HeadSpecialityAdmin)
admin.site.register(AddressObjectService, AddressObjectServiceAdmin)