from core.admin.models import *

__author__ = 'sergio'


admin.site.register(LegalEntity, LegalEntityAdmin)
admin.site.register(HealthObjectType, HealthObjectTypeAdmin)
admin.site.register(HealingObject, HealingObjectAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(AddressObject, AddressObjectAdmin)
admin.site.register(StreetObject, StreetObjectAdmin)
admin.site.register(DistrictObject, DistrictObjectAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ClosingReason, ClosingReasonAdmin)