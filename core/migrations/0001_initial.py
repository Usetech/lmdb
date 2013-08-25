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
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['HealthObjectType'])

        # Adding model 'Position'
        db.create_table(u'core_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['Position'])

        # Adding model 'ServiceType'
        db.create_table(u'core_servicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['ServiceType'])

        # Adding model 'StreetObject'
        db.create_table(u'core_streetobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bti_id', self.gf('django.db.models.fields.CharField')(max_length=16, unique=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('iname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'core', ['StreetObject'])

        # Adding model 'DistrictObject'
        db.create_table(u'core_districtobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'core', ['DistrictObject'])

        # Adding model 'AddressObject'
        db.create_table(u'core_addressobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('bti_id', self.gf('django.db.models.fields.CharField')(max_length=16, unique=True, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.DistrictObject'], null=True, blank=True)),
            ('city_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('street', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.StreetObject'])),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('house_letter', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('housing', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('full_address_string', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['AddressObject'])

        # Adding index on 'AddressObject', fields ['house', 'house_letter', 'housing', 'building', 'street']
        db.create_index(u'core_addressobject', ['house', 'house_letter', 'housing', 'building', 'street_id'])

        # Adding model 'LegalEntity'
        db.create_table(u'core_legalentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chief_original_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('chief_first_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_middle_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_last_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('chief_position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Position'], null=True, blank=True)),
            ('chief_phone', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('original_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('ogrn_code', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('inn_code', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('jur_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='registered_entities', null=True, to=orm['core.AddressObject'])),
            ('fact_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='operating_entities', null=True, to=orm['core.AddressObject'])),
            ('original_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('errors', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('manager_user', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='OK', max_length=5, db_index=True)),
        ))
        db.send_create_signal(u'core', ['LegalEntity'])

        # Adding model 'Service'
        db.create_table(u'core_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('chief_original_name', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('chief_first_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_middle_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_last_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('chief_sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('chief_position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Position'], null=True, blank=True)),
            ('chief_phone', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('healing_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['core.HealingObject'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='healing_objects', to=orm['core.ServiceType'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('site_url', self.gf('django.db.models.fields.URLField')(max_length=1024, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('workdays', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('workhours', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('daysoff', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('daysoff_restrictions', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('specialization', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('paid_services', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('free_services', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('drug_provisioning', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('hospital_beds', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('departments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('hospital_levels', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('tour', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('receipes_provisioning', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('drugstore_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('hospital_type', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding unique constraint on 'Service', fields ['healing_object', 'service']
        db.create_unique(u'core_service', ['healing_object_id', 'service_id'])

        # Adding model 'HealingObject'
        db.create_table(u'core_healingobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('object_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='healing_objects', to=orm['core.HealthObjectType'])),
            ('legal_entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='healing_objects', null=True, to=orm['core.LegalEntity'])),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AddressObject'], null=True, blank=True)),
            ('original_address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('global_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('errors', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='branches', null=True, to=orm['core.HealingObject'])),
            ('manager_user', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='OK', max_length=5, db_index=True)),
        ))
        db.send_create_signal(u'core', ['HealingObject'])


    def backwards(self, orm):
        # Removing unique constraint on 'Service', fields ['healing_object', 'service']
        db.delete_unique(u'core_service', ['healing_object_id', 'service_id'])

        # Removing index on 'AddressObject', fields ['house', 'house_letter', 'housing', 'building', 'street']
        db.delete_index(u'core_addressobject', ['house', 'house_letter', 'housing', 'building', 'street_id'])

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
            'Meta': {'object_name': 'AddressObject', 'index_together': "[['house', 'house_letter', 'housing', 'building', 'street']]"},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'bti_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'building': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'city_type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.DistrictObject']", 'null': 'True', 'blank': 'True'}),
            'full_address_string': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'house_letter': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'housing': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'street': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.StreetObject']"}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        u'core.districtobject': {
            'Meta': {'object_name': 'DistrictObject'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.healingobject': {
            'Meta': {'object_name': 'HealingObject'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AddressObject']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'global_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'legal_entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'null': 'True', 'to': u"orm['core.LegalEntity']"}),
            'manager_user': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'object_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.HealthObjectType']"}),
            'original_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'branches'", 'null': 'True', 'to': u"orm['core.HealingObject']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '5', 'db_index': 'True'})
        },
        u'core.healthobjecttype': {
            'Meta': {'object_name': 'HealthObjectType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.legalentity': {
            'Meta': {'object_name': 'LegalEntity'},
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_original_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'chief_position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']", 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fact_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'operating_entities'", 'null': 'True', 'to': u"orm['core.AddressObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inn_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'jur_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registered_entities'", 'null': 'True', 'to': u"orm['core.AddressObject']"}),
            'manager_user': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'ogrn_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'original_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '5', 'db_index': 'True'})
        },
        u'core.position': {
            'Meta': {'object_name': 'Position'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.service': {
            'Meta': {'unique_together': "(('healing_object', 'service'),)", 'object_name': 'Service'},
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'chief_original_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'chief_position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']", 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'daysoff': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'daysoff_restrictions': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'drug_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'drugstore_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'free_services': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'healing_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['core.HealingObject']"}),
            'hospital_beds': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'hospital_levels': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'hospital_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paid_services': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'receipes_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.ServiceType']"}),
            'site_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'specialization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tour': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'workdays': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'workhours': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'core.servicetype': {
            'Meta': {'object_name': 'ServiceType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.streetobject': {
            'Meta': {'object_name': 'StreetObject'},
            'bti_id': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['core']