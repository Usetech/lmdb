# Create your views here.
from annoying.decorators import render_to
from core.models import LegalEntity

@render_to("legal_entity.html")
def legal_entity(request, id):
    le = LegalEntity.objects.get(pk=id)
    return {
        'object': le,
        'healing_centers': le.healing_objects.filter(parent_id__isnull=True)
    }