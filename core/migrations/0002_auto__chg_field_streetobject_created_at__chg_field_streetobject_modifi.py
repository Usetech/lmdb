# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'StreetObject', fields ['name', 'type']
        db.delete_unique(u'core_streetobject', ['name', 'type'])


        # Changing field 'StreetObject.created_at'
        db.alter_column(u'core_streetobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'StreetObject.modified_at'
        db.alter_column(u'core_streetobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'LegalEntity.created_at'
        db.alter_column(u'core_legalentity', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'LegalEntity.modified_at'
        db.alter_column(u'core_legalentity', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'ServiceType.created_at'
        db.alter_column(u'core_servicetype', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'ServiceType.modified_at'
        db.alter_column(u'core_servicetype', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'HealingObject.created_at'
        db.alter_column(u'core_healingobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'HealingObject.modified_at'
        db.alter_column(u'core_healingobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Position.created_at'
        db.alter_column(u'core_position', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Position.modified_at'
        db.alter_column(u'core_position', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Service.created_at'
        db.alter_column(u'core_service', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Service.modified_at'
        db.alter_column(u'core_service', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'DistrictObject.created_at'
        db.alter_column(u'core_districtobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'DistrictObject.modified_at'
        db.alter_column(u'core_districtobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'AddressObject.created_at'
        db.alter_column(u'core_addressobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'AddressObject.modified_at'
        db.alter_column(u'core_addressobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'HealthObjectType.created_at'
        db.alter_column(u'core_healthobjecttype', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'HealthObjectType.modified_at'
        db.alter_column(u'core_healthobjecttype', 'modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    def backwards(self, orm):

        # Changing field 'StreetObject.created_at'
        db.alter_column(u'core_streetobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'StreetObject.modified_at'
        db.alter_column(u'core_streetobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())
        # Adding unique constraint on 'StreetObject', fields ['name', 'type']
        db.create_unique(u'core_streetobject', ['name', 'type'])


        # Changing field 'LegalEntity.created_at'
        db.alter_column(u'core_legalentity', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'LegalEntity.modified_at'
        db.alter_column(u'core_legalentity', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ServiceType.created_at'
        db.alter_column(u'core_servicetype', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ServiceType.modified_at'
        db.alter_column(u'core_servicetype', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HealingObject.created_at'
        db.alter_column(u'core_healingobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HealingObject.modified_at'
        db.alter_column(u'core_healingobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Position.created_at'
        db.alter_column(u'core_position', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Position.modified_at'
        db.alter_column(u'core_position', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Service.created_at'
        db.alter_column(u'core_service', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Service.modified_at'
        db.alter_column(u'core_service', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'DistrictObject.created_at'
        db.alter_column(u'core_districtobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'DistrictObject.modified_at'
        db.alter_column(u'core_districtobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'AddressObject.created_at'
        db.alter_column(u'core_addressobject', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'AddressObject.modified_at'
        db.alter_column(u'core_addressobject', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HealthObjectType.created_at'
        db.alter_column(u'core_healthobjecttype', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'HealthObjectType.modified_at'
        db.alter_column(u'core_healthobjecttype', 'modified_at', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'core.addressobject': {
            'Meta': {'object_name': 'AddressObject'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DistrictObject']"}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'house_letter': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'housing': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.StreetObject']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'core.districtobject': {
            'Meta': {'object_name': 'DistrictObject'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.healingobject': {
            'Meta': {'object_name': 'HealingObject'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AddressObject']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'global_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_entities': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'healing_objects'", 'symmetrical': 'False', 'through': u"orm['core.Service']", 'to': u"orm['core.LegalEntity']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'object_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.HealthObjectType']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'core.healthobjecttype': {
            'Meta': {'object_name': 'HealthObjectType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.legalentity': {
            'Meta': {'object_name': 'LegalEntity'},
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'chief_speciality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fact_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'operating_entities'", 'null': 'True', 'to': u"orm['core.AddressObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inn_code': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'jur_address': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registered_entities'", 'to': u"orm['core.AddressObject']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ogrn_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'core.position': {
            'Meta': {'object_name': 'Position'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.service': {
            'Meta': {'unique_together': "(('legal_entity', 'healing_object', 'service'),)", 'object_name': 'Service'},
            'aptheke_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'chief_speciality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'daysoff': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'daysoff_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'drug_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'free_services': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'healing_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['core.HealingObject']"}),
            'hospital_beds': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'hospital_levels': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['core.LegalEntity']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'paid_services': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'receipes_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.ServiceType']"}),
            'site_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'specialization': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'tour': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'workdays': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'workhours': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.servicetype': {
            'Meta': {'object_name': 'ServiceType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.streetobject': {
            'Meta': {'object_name': 'StreetObject'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['core']