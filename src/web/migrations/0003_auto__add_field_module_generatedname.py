# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Module.generatedname'
        db.add_column(u'web_module', 'generatedname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Module.generatedname'
        db.delete_column(u'web_module', 'generatedname')


    models = {
        u'web.module': {
            'Meta': {'object_name': 'Module'},
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'author_acronym': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'average_rating': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documentation': ('django.db.models.fields.TextField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'generatedname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'number_of_ratings': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sourcecode': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tagged_modules'", 'symmetrical': 'False', 'to': u"orm['web.Tag']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'web.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['web']