# coding=utf-8
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from guardian.admin import GuardedModelAdmin
from guardian.models import UserObjectPermission
from guardian.utils import get_user_obj_perms_model
from core.admin.forms import ServiceForm, HealingObjectForm, NamedModelForm, get_user_manager_form, user_manager_fieldset, user_manager_fields
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


class BaseModelAdmin(admin.ModelAdmin):
    model = BaseModel
    base_fields = ('created_at', 'modified_at', 'deleted_at')
    list_display = ('modified_at', )
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
    change_list_template = "admin/change_list_filter_sidebar.html"
    #change_list_filter_template = "admin/filter_listing.html"


class BaseGuardedModelAdmin(GuardedModelAdmin, BaseModelAdmin):
    def queryset(self, request):
        qs = super(BaseGuardedModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        user_model = get_user_obj_perms_model(self.model)
        user_obj_perms_queryset = (user_model.objects
                                   .filter(user=request.user)
                                   .filter(permission__content_type=ContentType.objects.get_for_model(self.model))).values_list('object_pk', flat=True)
        #if len(user_obj_perms_queryset): #если наложены ограничения - фильтруем
        return qs.filter(pk__in=map(int, user_obj_perms_queryset))


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
        ('paid_services', ),
        ('free_services',),
        ('drug_provisioning', 'hospital_beds'),
        ('departments',),
        ('hospital_levels',),
        ('tour',),
        ('receipes_provisioning',),
        ('drugstore_type',),
        ('hospital_type',),
    )
    suit_classes = 'suit-tab suit-tab-services'
    extra = 0


class HealingObjectInline(admin.StackedInline):
    model = HealingObject
    form = get_user_manager_form(HealingObject, 'change_healingobject', u"Управляющие объектами здравоохранения",
                                 u"Реестр МУ: требуется актуализация информации по объекту здравоохранения", "email/welcome_healingobject.html")
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
             ) + user_manager_fields
    extra = 0
    suit_classes = 'suit-tab suit-tab-healings'


class LegalEntityAdmin(BaseGuardedModelAdmin):

    model = LegalEntity
    form = get_user_manager_form(LegalEntity, 'change_legalentity', u"Управляющие юрлицами",
                                 u"Реестр МУ: требуется актуализация информации по юридическому лицу", "email/welcome_legalentity.html")
    date_hierarchy = 'modified_at'
    search_fields = ('name', 'chief_original_name', 'manager_user')
    list_filter = ('deleted_at',)
    list_display_links = ['id', 'name']
    list_display = ('id', 'name', 'chief_original_name', 'manager_user', ) + BaseModelAdmin.list_display
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
        chief_fields,
        user_manager_fieldset
    )

    change_list_template = "admin/change_list_filter_sidebar.html"
    change_list_filter_template = "admin/filter_listing.html"

    def save_model(self, request, obj, form, change):
        obj.save()
        try:
            UserObjectPermission.objects.assign_perm('change_legalentity', request.user, obj)
        except:
            pass

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


class ServiceAdmin(BaseGuardedModelAdmin):
    model = Service
    form = ServiceForm
    raw_id_fields = ('healing_object',)
    related_lookup_fields = {
        'fk': ['healing_object']
    }
    list_filter = ('modified_at', 'deleted_at', 'service')
    list_display = ('healing_object', 'service', 'modified_at')
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ('healing_object',),
                    ('service',),
                    ('phone',),
                    ('fax',),
                    ('site_url',),
                    ('info',),
                    ('workdays', 'workhours'),
                    ('daysoff', 'daysoff_restrictions')
                )
            }
        ),
        (
            u"Руководитель ",
            {
                'fields': (
                    ("chief_original_name",),
                    ("chief_sex", "chief_position"),
                )
            }
        ),
        (
            u"Информация по услуге",
            {
                'fields': (
                    ('specialization', ),
                    ('paid_services', ),
                    ('free_services',),
                    ('drug_provisioning', 'hospital_beds'),
                    ('departments',),
                    ('hospital_levels',),
                    ('tour',),
                    ('receipes_provisioning',),
                    ('drugstore_type',),
                    ('hospital_type',),
                )
            }
        ),
    )


class HealingObjectAdmin(BaseGuardedModelAdmin):
    model = HealingObject
    form = get_user_manager_form(HealingObject, 'change_healingobject', u"Управляющие объектами здравоохранения",
                                 u"Реестр МУ: требуется актуализация информации по объекту здравоохранения", "email/welcome_healingobject.html")
    list_filter = ('object_type',)
    list_display_links = ['object_type', 'name']
    suit_form_tabs = (('general', u'Основные'), ('services', u'Услуги'))
    raw_id_fields = ('address', 'parent', 'legal_entity')
    readonly_fields = BaseGuardedModelAdmin.readonly_fields + ('errors', 'original_address')
    fieldsets = BaseModelAdmin.fieldsets_tab + (
        (
            u"Основные параметры",
            {
                'classes': ('suit-tab suit-tab-general',),
                'fields': (
                    ('parent',),
                    ('legal_entity',),
                    ('object_type',),
                    ('address', ),
                    ('full_name',),
                    ('name', ),
                    ('short_name',),
                    ('global_id',),
                    ('info', ),
                    ('errors', ),
                    ('original_address', )
                )
            }
        ),
        user_manager_fieldset
    )
    search_fields = ('object_type__name', 'name', 'address__street__name')
    list_display = ('object_type', 'name', 'address', 'manager_user', 'modified_at', 'deleted_at', 'errors')
    inlines = [HealingObjectServiceInline]

    def save_model(self, request, obj, form, change):
        obj.save()
        try:
            UserObjectPermission.objects.assign_perm('change_healingobject', request.user, obj)
        except:
            pass

        if len(obj.services.all()):
            [UserObjectPermission.objects.assign_perm('change_service', request.user, service) for service in obj.services.all()]
            [UserObjectPermission.objects.assign_perm('delete_service', request.user, service) for service in obj.services.all()]