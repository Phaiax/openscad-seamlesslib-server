# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Module.name'
        db.delete_column(u'web_module', 'name')

        # Adding field 'Module.title'
        db.add_column(u'web_module', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Module.modulename'
        db.add_column(u'web_module', 'modulename',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40),
                      keep_default=False)


        # Changing field 'Module.author'
        db.alter_column(u'web_module', 'author', self.gf('django.db.models.fields.CharField')(max_length=40))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Module.name'
        raise RuntimeError("Cannot reverse this migration. 'Module.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Module.name'
        db.add_column(u'web_module', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=40),
                      keep_default=False)

        # Deleting field 'Module.title'
        db.delete_column(u'web_module', 'title')

        # Deleting field 'Module.modulename'
        db.delete_column(u'web_module', 'modulename')


        # Changing field 'Module.author'
        db.alter_column(u'web_module', 'author', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'web.module': {
            'Meta': {'object_name': 'Module'},
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'author_acronym': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'average_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documentation': ('django.db.models.fields.TextField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modulename': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'number_of_ratings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sourcecode': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tagged_modules'", 'symmetrical': 'False', 'to': u"orm['web.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'uniquename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'web.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['web']