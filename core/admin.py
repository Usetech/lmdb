# coding=utf-8
from itertools import groupby
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from guardian.admin import GuardedModelAdmin
from guardian.utils import get_user_obj_perms_model
from core.models import LegalEntity, AddressObject, BaseModel, HealthObjectType, Position, ServiceType

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


class LegalEntityAdmin(BaseGuardedModelAdmin):
    model = LegalEntity
    date_hierarchy = "created_at"
    list_display = ("name", "chief_first_name", "jur_address",)+BaseModelAdmin.list_display
    #user_can_access_owned_objects_only = True
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ("name",),
                    ("ogrn_code", "inn_code"),
                    ("chief_first_name",),
                    ("jur_address",),
                    ("fact_address",)
                )
            }
        ),
    )


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


class HealthObjectTypeAdmin(NamedModelAdmin):
    model = HealthObjectType


class PositionAdmin(NamedModelAdmin):
    model = Position


class ServiceTypeAdmin(NamedModelAdmin):
    model = ServiceType


admin.site.register(LegalEntity, LegalEntityAdmin)
admin.site.register(HealthObjectType, HealthObjectTypeAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)