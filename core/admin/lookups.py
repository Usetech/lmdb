from selectable.base import ModelLookup
from selectable.registry import registry
from core.models import LegalEntity, AddressObject, HealingObject, StreetObject

__author__ = 'sergio'


class LegalEntityLookup(ModelLookup):
    model = LegalEntity
    search_fields = ('name__icontains',)


class StreetLookup(ModelLookup):
    model = StreetObject
    search_fields = ('name__icontains',)


class AddressObjectLookup(ModelLookup):
    model = AddressObject
    search_fields = ('zip_code', 'area__icontains', 'city__icontains', 'street__iname__startswith', 'full_address_string__startswith')

    def get_query(self, request, term):
        term_parts = term.split(" ")
        if len(term_parts) and term_parts[-1].isdigit():
            term = " ".join(term_parts[:-1])
            qs = super(AddressObjectLookup, self).get_query(request, term)
            return qs.filter(house__startswith=term_parts[-1])

        return super(AddressObjectLookup, self).get_query(request, term)


class HealingObjectLookup(ModelLookup):
    model = HealingObject
    search_fields = ('full_name__icontains', 'name__icontains', 'short_name__icontains')

registry.register(LegalEntityLookup)
registry.register(AddressObjectLookup)
registry.register(HealingObjectLookup)
registry.register(StreetLookup)
