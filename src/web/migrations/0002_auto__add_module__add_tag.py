# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Module'
        db.create_table(u'web_module', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author_acronym', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sourcecode', self.gf('django.db.models.fields.TextField')()),
            ('documentation', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('auth_code', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('average_rating', self.gf('django.db.models.fields.FloatField')()),
            ('number_of_ratings', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'web', ['Module'])

        # Adding M2M table for field tags on 'Module'
        m2m_table_name = db.shorten_name(u'web_module_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm[u'web.module'], null=False)),
            ('tag', models.ForeignKey(orm[u'web.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module_id', 'tag_id'])

        # Adding model 'Tag'
        db.create_table(u'web_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'web', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'Module'
        db.delete_table(u'web_module')

        # Removing M2M table for field tags on 'Module'
        db.delete_table(db.shorten_name(u'web_module_tags'))

        # Deleting model 'Tag'
        db.delete_table(u'web_tag')


    models = {
        u'web.module': {
            'Meta': {'object_name': 'Module'},
            'auth_code': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'author_acronym': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'average_rating': ('django.db.models.fields.FloatField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documentation': ('django.db.models.fields.TextField', [], {}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'number_of_ratings': ('django.db.models.fields.IntegerField', [], {}),
            'sourcecode': ('django.db.models.fields.TextField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tagged_modules'", 'symmetrical': 'False', 'to': u"orm['web.Tag']"}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        u'web.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['web']