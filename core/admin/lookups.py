from selectable.base import LookupBase
from core.models import LegalEntity

__author__ = 'sergio'


class LegalEntityLookup(LookupBase):
    model = LegalEntity
    search_fields = ('name__icontains', 'chief_original_name__icontains')