# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AddressObjectType'
        db.create_table(u'core_addressobjecttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['AddressObjectType'])

        # Adding model 'HeadSpeciality'
        db.create_table(u'core_headspeciality', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['HeadSpeciality'])

        # Adding model 'AddressObjectService'
        db.create_table(u'core_addressobjectservice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'core', ['AddressObjectService'])

        # Adding model 'LegalEntity'
        db.create_table(u'core_legalentity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('ogrn_code', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('inn_code', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('chief_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('jur_address', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('fact_address', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('head_physician', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('reception_phone', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('registry_phone', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('worktime', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['LegalEntity'])

        # Adding model 'AddressObject'
        db.create_table(u'core_addressobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address_objects', to=orm['core.LegalEntity'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='address_objects', to=orm['core.AddressObjectType'])),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('okrug', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('chief', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('chief_sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('chief_speciality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.HeadSpeciality'])),
        ))
        db.send_create_signal(u'core', ['AddressObject'])

        # Adding M2M table for field services on 'AddressObject'
        m2m_table_name = db.shorten_name(u'core_addressobject_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('addressobject', models.ForeignKey(orm[u'core.addressobject'], null=False)),
            ('addressobjectservice', models.ForeignKey(orm[u'core.addressobjectservice'], null=False))
        ))
        db.create_unique(m2m_table_name, ['addressobject_id', 'addressobjectservice_id'])


    def backwards(self, orm):
        # Deleting model 'AddressObjectType'
        db.delete_table(u'core_addressobjecttype')

        # Deleting model 'HeadSpeciality'
        db.delete_table(u'core_headspeciality')

        # Deleting model 'AddressObjectService'
        db.delete_table(u'core_addressobjectservice')

        # Deleting model 'LegalEntity'
        db.delete_table(u'core_legalentity')

        # Deleting model 'AddressObject'
        db.delete_table(u'core_addressobject')

        # Removing M2M table for field services on 'AddressObject'
        db.delete_table(db.shorten_name(u'core_addressobject_services'))


    models = {
        u'core.addressobject': {
            'Meta': {'object_name': 'AddressObject'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'chief': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'chief_sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'chief_speciality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.HeadSpeciality']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'okrug': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_objects'", 'to': u"orm['core.LegalEntity']"}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'address_objects'", 'symmetrical': 'False', 'to': u"orm['core.AddressObjectService']"}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'address_objects'", 'to': u"orm['core.AddressObjectType']"})
        },
        u'core.addressobjectservice': {
            'Meta': {'object_name': 'AddressObjectService'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.addressobjecttype': {
            'Meta': {'object_name': 'AddressObjectType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.headspeciality': {
            'Meta': {'object_name': 'HeadSpeciality'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'core.legalentity': {
            'Meta': {'object_name': 'LegalEntity'},
            'chief_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fact_address': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'head_physician': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inn_code': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'jur_address': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'ogrn_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'reception_phone': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'registry_phone': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'worktime': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']