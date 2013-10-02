# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DispSpecialization'
        db.create_table(u'core_dispspecialization', (
            (u'specialization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Specialization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['DispSpecialization'])

        # Adding model 'StatSpecialization'
        db.create_table(u'core_statspecialization', (
            (u'specialization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Specialization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['StatSpecialization'])

        # Adding model 'MaternitySpecialization'
        db.create_table(u'core_maternityspecialization', (
            (u'specialization_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Specialization'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'core', ['MaternitySpecialization'])

        # Adding model 'Specialization'
        db.create_table(u'core_specialization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16, unique=True, null=True)),
        ))
        db.send_create_signal(u'core', ['Specialization'])

        # Adding field 'Service.mat_specialization'
        db.add_column(u'core_service', 'mat_specialization',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='mat_specialization', null=True, to=orm['core.MaternitySpecialization']),
                      keep_default=False)

        # Adding field 'Service.disp_specialization'
        db.add_column(u'core_service', 'disp_specialization',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='disp_specialization', null=True, to=orm['core.DispSpecialization']),
                      keep_default=False)

        # Adding field 'Service.stat_specialization'
        db.add_column(u'core_service', 'stat_specialization',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='stat_specialization', null=True, to=orm['core.StatSpecialization']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'DispSpecialization'
        db.delete_table(u'core_dispspecialization')

        # Deleting model 'StatSpecialization'
        db.delete_table(u'core_statspecialization')

        # Deleting model 'MaternitySpecialization'
        db.delete_table(u'core_maternityspecialization')

        # Deleting model 'Specialization'
        db.delete_table(u'core_specialization')

        # Deleting field 'Service.mat_specialization'
        db.delete_column(u'core_service', 'mat_specialization_id')

        # Deleting field 'Service.disp_specialization'
        db.delete_column(u'core_service', 'disp_specialization_id')

        # Deleting field 'Service.stat_specialization'
        db.delete_column(u'core_service', 'stat_specialization_id')


    models = {
        u'core.addressobject': {
            'Meta': {'object_name': 'AddressObject', 'index_together': "[['house', 'house_letter', 'housing', 'building', 'street']]"},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AreaObject']", 'null': 'True', 'blank': 'True'}),
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
        u'core.areaobject': {
            'Meta': {'object_name': 'AreaObject'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.closingreason': {
            'Meta': {'object_name': 'ClosingReason'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.dispspecialization': {
            'Meta': {'object_name': 'DispSpecialization', '_ormbases': [u'core.Specialization']},
            u'specialization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Specialization']", 'unique': 'True', 'primary_key': 'True'})
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
            'closed_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'closing_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'closing_reason'", 'null': 'True', 'to': u"orm['core.ClosingReason']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'global_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legal_entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'healing_objects'", 'null': 'True', 'to': u"orm['core.LegalEntity']"}),
            'manager_user': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'object_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.HealthObjectType']"}),
            'original_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'branches'", 'null': 'True', 'to': u"orm['core.HealingObject']"}),
            'reopened_at': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OK'", 'max_length': '5', 'db_index': 'True'})
        },
        u'core.healthobjecttype': {
            'Meta': {'object_name': 'HealthObjectType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.legalentity': {
            'Meta': {'object_name': 'LegalEntity'},
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_original_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']", 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fact_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'operating_entities'", 'null': 'True', 'to': u"orm['core.AddressObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'inn_code': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'jur_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'registered_entities'", 'null': 'True', 'to': u"orm['core.AddressObject']"}),
            'manager_user': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000'}),
            'ogrn_code': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'original_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'original_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'\\xd0\\x90'", 'max_length': '5', 'db_index': 'True'})
        },
        u'core.maternityspecialization': {
            'Meta': {'object_name': 'MaternitySpecialization', '_ormbases': [u'core.Specialization']},
            u'specialization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Specialization']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.position': {
            'Meta': {'object_name': 'Position'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.service': {
            'Meta': {'unique_together': "(('healing_object', 'service'),)", 'object_name': 'Service'},
            'beneficial_drug_prescriptions': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'chief_first_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_last_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_middle_name': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_original_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'chief_phone': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'chief_position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Position']", 'null': 'True', 'blank': 'True'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'departments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disp_specialization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'disp_specialization'", 'null': 'True', 'to': u"orm['core.DispSpecialization']"}),
            'drug_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'drugstore_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'free_services': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'healing_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['core.HealingObject']"}),
            'hospital_beds': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'hospital_levels': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'hospital_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'mat_specialization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mat_specialization'", 'null': 'True', 'to': u"orm['core.MaternitySpecialization']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'paid_services': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'receipes_provisioning': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'healing_objects'", 'to': u"orm['core.ServiceType']"}),
            'site_url': ('django.db.models.fields.URLField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'specialization': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'stat_specialization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stat_specialization'", 'null': 'True', 'to': u"orm['core.StatSpecialization']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'\\xd0\\x90'", 'max_length': '5', 'db_index': 'True'}),
            'tour': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'workhours': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'workhours_clarification': ('django.db.models.fields.CharField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'})
        },
        u'core.servicetype': {
            'Meta': {'object_name': 'ServiceType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.specialization': {
            'Meta': {'object_name': 'Specialization'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'core.statspecialization': {
            'Meta': {'object_name': 'StatSpecialization', '_ormbases': [u'core.Specialization']},
            u'specialization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Specialization']", 'unique': 'True', 'primary_key': 'True'})
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