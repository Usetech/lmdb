# coding=utf-8
from itertools import groupby
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from guardian.admin import GuardedModelAdmin
from guardian.utils import get_user_obj_perms_model
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

class BaseGuardedModelAdmin(GuardedModelAdmin, BaseModelAdmin):
    def queryset(self, request):
        qs = super(BaseGuardedModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        user_model = get_user_obj_perms_model(self.model)
        user_obj_perms_queryset = (user_model.objects
            .filter(user=request.user)
            .filter(permission__content_type=ContentType.objects.get_for_model(self.model)))
        return qs.filter(pk__in=user_obj_perms_queryset)

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


class LegalEntityAdmin(BaseGuardedModelAdmin):
    model = LegalEntity
    date_hierarchy = "created_at"
    list_display = ("name", "chief_name", "jur_address",)+BaseModelAdmin.list_display
    #user_can_access_owned_objects_only = True
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