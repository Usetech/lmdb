# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HealthObjectType'
        db.create_table(u'core_healthobjecttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['HealthObjectType'])

        # Adding model 'Position'
        db.create_table(u'core_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['Position'])

        # Adding model 'ServiceType'
        db.create_table(u'core_servicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['ServiceType'])

        # Adding model 'StreetObject'
        db.create_table(u'core_streetobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['StreetObject'])

        # Adding model 'DistrictObject'
        db.create_table(u'core_districtobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['DistrictObject'])

        # Adding model 'AddressObject'
        db.create_table(u'core_addressobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.DistrictObject'])),
            ('city_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.StreetObject'])),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('house_letter', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('housing', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
        ))
        db.send_create_signal(u'core', ['AddressObject'])

        # Adding model 'LegalEntity'
        db.create_table(u'core_legalentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chief_first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_middle_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('chief_speciality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Position'])),
            ('chief_phone', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('ogrn_code', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('inn_code', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('jur_address', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registered_entities', to=orm['core.AddressObject'])),
            ('fact_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='operating_entities', null=True, to=orm['core.AddressObject'])),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['LegalEntity'])

        # Adding model 'Service'
        db.create_table(u'core_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chief_first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_middle_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('chief_speciality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Position'])),
            ('chief_phone', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('legal_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['core.LegalEntity'])),
            ('healing_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['core.HealingObject'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='healing_objects', to=orm['core.ServiceType'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('site_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('workdays', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('workhours', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('daysoff', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('daysoff_restrictions', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('specialization', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('paid_services', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('free_services', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('drug_provisioning', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('hospital_beds', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('departments', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('hospital_levels', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('tour', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('receipes_provisioning', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('aptheke_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding unique constraint on 'Service', fields ['legal_entity', 'healing_object', 'service']
        db.create_unique(u'core_service', ['legal_entity_id', 'healing_object_id', 'service_id'])

        # Adding model 'HealingObject'
        db.create_table(u'core_healingobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AddressObject'])),
            ('object_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='healing_objects', to=orm['core.HealthObjectType'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('global_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['HealingObject'])


    def backwards(self, orm):
        # Removing unique constraint on 'Service', fields ['legal_entity', 'healing_object', 'service']
        db.delete_unique(u'core_service', ['legal_entity_id', 'healing_object_id', 'service_id'])

        # Deleting model 'HealthObjectType'
        db.delete_table(u'core_healthobjecttype')

        # Deleting model 'Position'
        db.delete_table(u'core_position')

        # Deleting model 'ServiceType'
        db.delete_table(u'core_servicetype')

        # Deleting model 'StreetObject'
        db.delete_table(u'core_streetobject')

        # Deleting model 'DistrictObject'
        db.delete_table(u'core_districtobject')

        # Deleting model 'AddressObject'
        db.delete_table(u'core_addressobject')

        # Deleting model 'LegalEntity'
        db.delete_table(u'core_legalentity')

        # Deleting model 'Service'
        db.delete_table(u'core_service')

        # Deleting model 'HealingObject'
        db.delete_table(u'core_healingobject')


    models = {
        u'core.addressobject': {
            'Meta': {'object_name': 'AddressObject'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DistrictObject']"}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'house_letter': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'housing': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        }
    }

    complete_apps = ['core']