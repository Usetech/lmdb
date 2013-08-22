from selectable.base import ModelLookup
from selectable.registry import registry
from core.models import LegalEntity, AddressObject

__author__ = 'sergio'


class LegalEntityLookup(ModelLookup):
    model = LegalEntity
    search_fields = ('name__icontains', 'chief_original_name__icontains',)


class AddressObjectLookup(ModelLookup):
    model = AddressObject
    search_fields = ('zip_code', 'area__icontains', 'city__icontains', 'street__name__icontains')


registry.register(LegalEntityLookup)
registry.register(AddressObjectLookup)
