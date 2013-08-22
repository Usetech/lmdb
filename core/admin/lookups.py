from selectable.base import LookupBase
from selectable.registry import registry
from core.models import LegalEntity

__author__ = 'sergio'


class LegalEntityLookup(LookupBase):
    model = LegalEntity
    search_fields = ('name__icontains', 'chief_original_name__icontains')

registry.register(LegalEntityLookup)
