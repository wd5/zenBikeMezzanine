# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'color'
        db.create_table('zenbicycle_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('zenbicycle', ['color'])

        # Adding model 'AbstractModelBicycle'
        db.create_table('zenbicycle_abstractmodelbicycle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('modelName', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('firm', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('features', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('zenbicycle', ['AbstractModelBicycle'])

        # Adding model 'bicycle'
        db.create_table('zenbicycle_bicycle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('numberFrame', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modelBicycle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zenbicycle.AbstractModelBicycle'])),
        ))
        db.send_create_signal('zenbicycle', ['bicycle'])

        # Adding M2M table for field colorBicycle on 'bicycle'
        db.create_table('zenbicycle_bicycle_colorBicycle', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bicycle', models.ForeignKey(orm['zenbicycle.bicycle'], null=False)),
            ('color', models.ForeignKey(orm['zenbicycle.color'], null=False))
        ))
        db.create_unique('zenbicycle_bicycle_colorBicycle', ['bicycle_id', 'color_id'])

        # Adding model 'incident'
        db.create_table('zenbicycle_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('placeText', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('placeOnMap', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('zenbicycle', ['incident'])


    def backwards(self, orm):
        
        # Deleting model 'color'
        db.delete_table('zenbicycle_color')

        # Deleting model 'AbstractModelBicycle'
        db.delete_table('zenbicycle_abstractmodelbicycle')

        # Deleting model 'bicycle'
        db.delete_table('zenbicycle_bicycle')

        # Removing M2M table for field colorBicycle on 'bicycle'
        db.delete_table('zenbicycle_bicycle_colorBicycle')

        # Deleting model 'incident'
        db.delete_table('zenbicycle_incident')


    models = {
        'zenbicycle.abstractmodelbicycle': {
            'Meta': {'object_name': 'AbstractModelBicycle'},
            'features': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'firm': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modelName': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'zenbicycle.bicycle': {
            'Meta': {'object_name': 'bicycle'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'colorBicycle': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['zenbicycle.color']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modelBicycle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zenbicycle.AbstractModelBicycle']"}),
            'numberFrame': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'zenbicycle.color': {
            'Meta': {'object_name': 'color'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'zenbicycle.incident': {
            'Meta': {'object_name': 'incident'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placeOnMap': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'placeText': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['zenbicycle']
