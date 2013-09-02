# coding=utf-8
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from guardian.admin import GuardedModelAdmin
from guardian.models import User
from guardian.shortcuts import get_perms
from guardian.utils import get_user_obj_perms_model
from core.admin.base import LinkedInline
from core.admin.filters import LegalEntityServiceTypeListFilter, HealingObjectServiceTypeListFilter
from core.admin.forms import ServiceForm, NamedModelForm, get_user_manager_form, user_manager_fieldset, user_manager_fields, AddressObjectForm
from core.admin.tools import StatusAdminMixin
from core.models import LegalEntity, AddressObject, BaseModel, HealthObjectType, Position, ServiceType, StreetObject, DistrictObject, Service, HealingObject

__author__ = 'sergio'

chief_fields = (
    u"Руководитель ",
    {
        'classes': ('suit-tab suit-tab-general ', 'grp-collapse grp-closed',),
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
    list_select_related = True
    fieldsets = (
        (u"", {
            'fields': (base_fields,),
            'classes': ('collapse',),
        }),
    )
    fieldsets_tab = (
        (u"", {
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
        ct = ContentType.objects.get_for_model(self.model)
        user_obj_perms_queryset = (user_model.objects
                                   .filter(user=request.user)
                                   .filter(permission__content_type=ct)).values_list('object_pk', flat=True)
        pname = '%s.viewall_%s' % (ct.app_label, ct.model)
        if request.user.has_perm(pname) and not len(user_obj_perms_queryset):
            return qs
        #if len(user_obj_perms_queryset): #если наложены ограничения - фильтруем
        return qs.filter(pk__in=map(int, user_obj_perms_queryset))

    def get_model_perms(self, request, *args, **kwargs):
        perms = admin.ModelAdmin.get_model_perms(self, request, *args, **kwargs)
        ct = ContentType.objects.get_for_model(self.model)
        perms['view'] = request.user.has_perm("%s.view_%s" % (ct.app_label, ct.model))
        # Грязный хак над grapelli
        perms['changeable'] = perms['change']
        perms['change'] = perms['view']
        # /Грязный хак над grapelli
        return perms

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + opts.get_change_permission()) or \
               request.user.has_perm(opts.app_label + '.view_' + opts.object_name.lower())

    def can_save_own(self, request, obj):
        return request.user.has_perm(self.opts.app_label + '.' + self.opts.get_change_permission(), obj)

    def can_save(self, request, obj):
        return self.can_save_own(request, obj)

    def save_model(self, request, obj, form, change):
        if change and (not request.user.is_superuser) and (not self.can_save(request, obj)):
            raise PermissionDenied
        obj.save()

    def get_readonly_fields(self, request, obj=None):
        opts = self.opts
        if (not request.user.is_superuser) and\
                (not request.user.has_perm(opts.app_label + '.' + opts.get_change_permission(), obj)) and\
                (not request.user.has_perm(opts.app_label + '.' + opts.get_add_permission(), obj)):
            return obj._meta.get_all_field_names()
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.model.objects.get(pk=object_id)
        opts = self.opts or {}
        if (not request.user.is_superuser) and\
                (not self.can_save(request, obj)):
            opts.readonly = True
        return super(BaseGuardedModelAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


class AddressObjectAdmin(BaseModelAdmin):
    model = AddressObject
    form = AddressObjectForm
    search_fields = ('street__name', 'district__name')
    list_select_related = True
    list_filter = ('city', 'district')
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры",
            {
                'fields': (
                    ('zip_code',),
                    ('area',),
                    ('city',),
                    ('city_type',),
                    ('district',),
                    ('street',),
                    ('house', 'house_letter'),
                    ('housing', 'building')
                )
            }
        ),
    )
    list_display = ('full_address_string', 'city', 'district', 'street', 'house', 'house_letter', 'housing', 'building')


class HealingObjectServiceInline(LinkedInline):
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
    ordering = ('service__name',)
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 0


class HealingObjectInline(LinkedInline):
    model = HealingObject
    form = get_user_manager_form(HealingObject, 'change_healingobject', u"Управляющие объектами здравоохранения",
                                 u"Реестр МУ: требуется актуализация информации по объекту здравоохранения",
                                 "email/welcome_healingobject.html")
    fields = (
                 ('status',),
                 ('object_type',),
                 ('address', ),
                 ('full_name',),
                 ('name',),
                 ('short_name',),
                 ('global_id',),
                 ('info', )
             ) + user_manager_fields

    ordering = ('name',)
    extra = 0
    suit_classes = 'suit-tab suit-tab-healings'


class LegalEntityAdmin(BaseGuardedModelAdmin, StatusAdminMixin):
    #model = LegalEntity
    form = get_user_manager_form(LegalEntity, 'change_legalentity', u"Управляющие юрлицами",
                                 u"Реестр МУ: требуется актуализация информации по юридическому лицу",
                                 "email/welcome_legalentity.html")
    search_fields = ('name', 'chief_original_name', 'manager_user', 'fact_address__full_address_string')
    list_filter = ('status', LegalEntityServiceTypeListFilter, 'fact_address__district')
    list_display_links = ['name']
    readonly_fields = BaseGuardedModelAdmin.readonly_fields + ('errors',)
    list_display = ('name', 'fact_address', 'show_number_healingobjects') + BaseModelAdmin.list_display + (
        'get_status_name',)
    suit_form_tabs = (('general', u'Основные'), ('healings', u'Объекты здравоохранения'))
    #user_can_access_owned_objects_only = True
    fieldsets = BaseModelAdmin.fieldsets_tab + (
        (
            u"Основные параметры",
            {
                'classes': ('suit-tab suit-tab-general',),
                'fields': (
                    ('status',),
                    ("name",),
                    ("ogrn_code",),
                    ("inn_code",),
                    ("jur_address",),
                    ("fact_address",),
                    ('errors',)
                )
            }
        ),
        chief_fields,
        user_manager_fieldset
    )

    def show_number_healingobjects(self, item):
        return item.number_healingobjects

    show_number_healingobjects.admin_order_field = 'number_healingobjects'
    show_number_healingobjects.short_description = u"Кол-во МУ"

    def queryset(self, request):
        return super(LegalEntityAdmin, self).queryset(request).annotate(
            number_healingobjects=Count('healing_objects')).select_related(
            'fact_address', 'fact_address__street')

    def can_save(self, request, obj):
        ct = ContentType.objects.get_for_model(HealingObject)
        return request.user.has_perm(self.opts.app_label + '.' + self.opts.get_change_permission(), obj) \
            or request.user.has_perm("%s.change_%s" % (ct.app_label, ct.model))

    def save_model(self, request, obj, form, change):
        super(LegalEntityAdmin, self).save_model(request, obj, form, change)

        if self.can_save_own(request, obj):
            try:
                if obj.manager_user:
                    usr = User.objects.get(email=obj.manager_user)
                else:
                    usr = None

                LegalEntity.objects.assign_permissions(obj, request.user, usr)
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
    search_fields = ("name", "iname")
    fieldsets = BaseModelAdmin.fieldsets + (
        (
            u"Основные параметры", {
                'fields': ("name", "type")
            }
        ),
    )
    list_filter = ("valid",)
    list_display = ("id", "iname", "name", "valid",) + BaseModelAdmin.list_display


class DistrictObjectAdmin(NamedModelAdmin):
    model = DistrictObject


class ServiceAdmin(BaseGuardedModelAdmin):
    model = Service
    form = ServiceForm
    list_filter = ('service', 'modified_at')
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
        chief_fields,
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


class HealingObjectAdmin(BaseGuardedModelAdmin, StatusAdminMixin):
    model = HealingObject
    form = get_user_manager_form(HealingObject, 'change_healingobject', u"Управляющие объектами здравоохранения",
                                 u"Реестр МУ: требуется актуализация информации по объекту здравоохранения",
                                 "email/welcome_healingobject.html")
    list_filter = ('status', HealingObjectServiceTypeListFilter, 'object_type',)
    suit_form_tabs = (('general', u'Основные'), ('services', u'Услуги'))
    search_fields = ('object_type__name', 'name', 'address__full_address_string')
    list_display = ('name', 'address', 'object_type', 'show_number_services', 'modified_at', 'get_status_name')
    readonly_fields = BaseGuardedModelAdmin.readonly_fields + ('errors', 'original_address')
    fieldsets = BaseModelAdmin.fieldsets_tab + (
        (
            u"Основные параметры",
            {
                'classes': ('suit-tab suit-tab-general',),
                'fields': (
                    ('status',),
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

    def show_number_services(self, item):
        return item.number_services

    show_number_services.admin_order_field = 'number_services'
    show_number_services.short_description = u"Кол-во услуг"

    def queryset(self, request):
        return super(HealingObjectAdmin, self).queryset(request).annotate(
            number_services=Count('services')).select_related('address',
                                                              'address__street',
                                                              'object_type')

    inlines = [HealingObjectServiceInline]

    def can_save(self, request, obj):
        ct = ContentType.objects.get_for_model(Service)
        return request.user.has_perm(self.opts.app_label + '.' + self.opts.get_change_permission(), obj) \
            or request.user.has_perm("%s.change_%s" % (ct.app_label, ct.model))

    def save_model(self, request, obj, form, change):
        obj.save()

        if self.can_save_own(request, obj):
            try:
                if obj.manager_user:
                    usr = User.objects.get(email=obj.manager_user)
                else:
                    usr = None

                HealingObject.objects.assign_permissions(obj, request.user, usr)
            except:
                pass