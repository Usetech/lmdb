# coding=utf-8
from itertools import groupby
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm, TextInput
from guardian.admin import GuardedModelAdmin
from guardian.utils import get_user_obj_perms_model
from suit.widgets import AutosizedTextarea, EnclosedInput
from core.models import LegalEntity, AddressObject, BaseModel, HealthObjectType, Position, ServiceType, StreetObject, DistrictObject, Service, HealingObject

__author__ = 'sergio'

chief_fields = (
    u"Руководитель ",
    {
        'classes': ('suit-tab suit-tab-general',),
        'fields': (
            ("chief_original_name",),
            ("chief_sex", "chief_position"),
        )
    }
)


class InfoForm(ModelForm):
    class Meta:
        widgets = {
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
        }


class HealingObjectForm(ModelForm):
    class Meta:
        widgets = {
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'full_name': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xxlarge'}),
            'name': TextInput(attrs={'class': 'input-xxlarge'}),
            'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
        }


class ServiceForm(InfoForm):
    class Meta:
        widgets = {
            'phone': EnclosedInput(prepend='icon-headphones'),
            'fax': EnclosedInput(prepend='icon-print'),
            'site_url': EnclosedInput(prepend='icon-globe'),
            'info': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'specialization': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'departments': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
        }


class NamedModelForm(ModelForm):
    class Meta:
        widgets = {
            'name': TextInput(attrs={'class': 'input-xxlarge'})
        }


class LegalEntityForm(ModelForm):
    class Meta:
        widgets = {
            'chief_original_name': TextInput(attrs={'class':'input-xxlarge'})
        }


class BaseModelAdmin(admin.ModelAdmin):
    model = BaseModel
    base_fields = ("created_at", "modified_at", "deleted_at")
    list_display = base_fields
    fieldsets = (
        (u'Создание/изменение/удаление', {
            'fields': (base_fields,),
            'classes': ('collapse',),
        }),
    )
    fieldsets_tab = (
        (u'Создание/изменение/удаление', {
            'fields': (base_fields,),
            'classes': ('collapse suit-tab suit-tab-general',),
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


class AddressObjectAdmin(BaseModelAdmin):
    model = AddressObject
    search_fields = ('street__name', 'district__name')
    raw_id_fields = ('street',)
    list_select_related = True
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ('zip_code',),
                    ('district',),
                    ('street',),
                    ('house', 'house_letter'),
                    ('housing', 'building')
                )
            }
        ),
    )
    list_display = ('district', 'street', 'house', 'house_letter', 'housing', 'building', 'full_address_string')


class HealingObjectServiceInline(admin.StackedInline):
    model = Service
    form = ServiceForm
    raw_id_fields = ('healing_object',)
    fields = (
        ('service', ),
        ('phone', ),
        ('fax',),
        ('site_url',),
        ('chief_original_name',),
        ('chief_sex', 'chief_position',),
        ('info',),
        ('workdays', 'workhours'),
        ('daysoff', 'daysoff_restrictions'),

        ('specialization', ),
        ('paid_services', 'free_services',),
        ('drug_provisioning', 'hospital_beds'),
        ('departments',),
        ('hospital_levels',),
        ('tour',),
        ('receipes_provisioning',),
        ('aptheke_type',),
    )
    suit_classes = 'suit-tab suit-tab-services'
    extra = 0


class HealingObjectInline(admin.StackedInline):
    model = HealingObject
    form = HealingObjectForm
    raw_id_fields = ('address',)
    related_lookup_fields = {
        'fk': ['address']
    }
    fields = (
        ('object_type',),
        ('address', ),
        ('full_name',),
        ('name',),
        ('short_name',),
        ('global_id',),
        ('info', )
    )
    extra = 0
    suit_classes = 'suit-tab suit-tab-healings'


class LegalEntityAdmin(BaseGuardedModelAdmin):
    model = LegalEntity
    form = LegalEntityForm
    date_hierarchy = "modified_at"
    search_fields = ('name',)
    list_display = ("name", "chief_original_name",) + BaseModelAdmin.list_display
    raw_id_fields = ('jur_address', 'fact_address')
    related_lookup_fields = {
        'fk': ['jur_address', 'fact_address']
    }
    suit_form_tabs = (('general', u'Основные'), ('healings', u'Объекты здравоохранения'))
    #user_can_access_owned_objects_only = True
    fieldsets = BaseModelAdmin.fieldsets_tab + (
        (
            u"Основные параметры",
            {
                'classes': ('suit-tab suit-tab-general',),
                'fields': (
                    ("name",),
                    ("ogrn_code",),
                    ("inn_code",),
                    ("jur_address",),
                    ("fact_address",)
                )
            }
        ),
        chief_fields
    )
    inlines = [HealingObjectInline]


class NamedModelAdmin(BaseModelAdmin):
    form = NamedModelForm
    date_hierarchy = "modified_at"
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


class StreetObjectAdmin(BaseModelAdmin):
    model = StreetObject
    date_hierarchy = "modified_at"
    search_fields = ("name", )
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры", {
                'fields': ("name", "type")
            }
        ),
    )
    list_filter = ("valid",)
    list_display = ("id", "name", "valid",) + BaseModelAdmin.list_display


class DistrictObjectAdmin(NamedModelAdmin):
    model = DistrictObject


class ServiceAdmin(BaseModelAdmin):
    model = Service
    raw_id_fields = ('healing_object',)
    related_lookup_fields = {
        'fk': ['healing_object']
    }
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ('healing_object', 'service'),
                    ('phone', 'fax', 'site_url'),
                    ('info',),
                    ('workdays', 'workhours'),
                    ('daysoff', 'daysoff_restrictions')
                )
            }
        ),
        chief_fields,
        (
            u"Информация по услуге",
            {
                'fields': (
                    ('specialization', ),
                    ('paid_services', 'free_services',),
                    ('drug_provisioning', 'hospital_beds'),
                    ('departments',),
                    ('hospital_levels',),
                    ('tour',),
                    ('receipes_provisioning',),
                    ('aptheke_type',),
                )
            }
        ),
    )


class HealingObjectAdmin(BaseModelAdmin):
    model = HealingObject
    form = HealingObjectForm
    list_filter = ('object_type',)
    suit_form_tabs = (('general', u'Основные'), ('services', u'Услуги'))
    raw_id_fields = ('address', 'parent')
    readonly_fields = ('errors', )
    fieldsets = BaseModelAdmin.fieldsets_tab + (
        (
            u"Основные параметры",
            {
                'classes': ('suit-tab suit-tab-general',),
                'fields': (
                    ('parent',),
                    ('object_type',),
                    ('address', ),
                    ('full_name',),
                    ('name', ),
                    ('short_name',),
                    ('global_id',),
                    ('info', ),
                    ('errors', )
                )
            }
        ),
    )
    search_fields = ('object_type__name', 'name', 'address__street__name')
    list_display = ('object_type', 'name', 'address', 'created_at', 'modified_at', 'deleted_at', 'errors')
    inlines = [HealingObjectServiceInline]


admin.site.register(LegalEntity, LegalEntityAdmin)
admin.site.register(HealthObjectType, HealthObjectTypeAdmin)
admin.site.register(HealingObject, HealingObjectAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(AddressObject, AddressObjectAdmin)
admin.site.register(StreetObject, StreetObjectAdmin)
admin.site.register(DistrictObject, DistrictObjectAdmin)
admin.site.register(Service, ServiceAdmin)