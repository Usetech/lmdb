# coding=utf-8
from django.contrib.admin import SimpleListFilter
from core.models import ServiceType, HealingObject, Service

__author__ = 'sergio'


class LegalEntityServiceTypeListFilter(SimpleListFilter):
    title = u"Вид услуги"
    parameter_name = 'service'

    def lookups(self, request, model_admin):
        return map(lambda st: (st.id, st.name), ServiceType.objects.all())

    def queryset(self, request, queryset):
        flt = request.GET.get(self.parameter_name)
        if not flt:
            return queryset

        le_ids = Service.objects.filter(service_id=flt).values('healing_object__legal_entity__id')
        return queryset.filter(pk__in=le_ids)


class HealingObjectServiceTypeListFilter(SimpleListFilter):
    title = u"Вид услуги"
    parameter_name = 'service'

    def lookups(self, request, model_admin):
        return map(lambda st: (st.id, st.name), ServiceType.objects.all())

    def queryset(self, request, queryset):
        flt = request.GET.get(self.parameter_name)
        if not flt:
            return queryset

        ids = Service.objects.filter(service_id=flt).values('healing_object_id')
        return queryset.filter(pk__in=ids)


class ErrorListFilter(SimpleListFilter):
    title = u"Записи с ошибками"
    parameter_name = 'errors'

    def lookups(self, request, model_admin):
        return (
            ("err", u"С любыми ошибками"),
            ("address", u"Без адреса"),
            ("legal_entity", u"Без юридического лица"),
        )

    def queryset(self, request, queryset):
        flt = request.GET.get(self.parameter_name)
        if not flt:
            return queryset

        if flt == "address":
            return queryset.filter(address__isnull=True)
        elif flt == "legal_entity":
            return queryset.filter(legal_entity__isnull=True)
        return queryset.filter(errors__isnull=False)