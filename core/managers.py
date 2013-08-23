from django.contrib.auth.models import User
from django.db.models import Manager
from guardian.models import UserObjectPermission

__author__ = 'sergio'


class ServiceManager(Manager):
    def assign_permissions(self, obj, user):
        if user:
            UserObjectPermission.objects.assign_perm('delete_service', user, obj)
            UserObjectPermission.objects.assign_perm('change_service', user, obj)


class HealingObjectManager(Manager):
    def assign_permissions(self, obj, saver, manager):
        from core.models import Service
        if saver:
            UserObjectPermission.objects.assign_perm('delete_healingobject', saver, obj)
            UserObjectPermission.objects.assign_perm('change_healingobject', saver, obj)
        if manager:
            UserObjectPermission.objects.assign_perm('delete_healingobject', manager, obj)
            UserObjectPermission.objects.assign_perm('change_healingobject', manager, obj)
            for s in obj.services.all():
                Service.objects.assign_permissions(s, manager)


class LegalEntityManager(Manager):
    def assign_permissions(self, obj, saver, manager):
        from core.models import HealingObject
        if saver:
            UserObjectPermission.objects.assign_perm('change_legalentity', saver, obj)

        if len(obj.healing_objects.all()):
            for ho in obj.healing_objects.all():
                HealingObject.objects.assign_permissions(ho, saver, None)
                HealingObject.objects.assign_permissions(ho, manager, None)
