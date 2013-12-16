# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DeskItem'
        db.create_table(u'deskitem_deskitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('at_dorm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('max_loan_duration', self.gf('timedelta.fields.TimedeltaField')(default=None, null=True)),
        ))
        db.send_create_signal(u'deskitem', ['DeskItem'])

        # Adding model 'DeskItemLoan'
        db.create_table(u'deskitem_deskitemloan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desk_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='desk_item_loans', to=orm['deskitem.DeskItem'])),
            ('resident', self.gf('django.db.models.fields.related.ForeignKey')(related_name='desk_item_loans', to=orm['residents.Resident'])),
            ('loaned_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('returned_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal(u'deskitem', ['DeskItemLoan'])


    def backwards(self, orm):
        # Deleting model 'DeskItem'
        db.delete_table(u'deskitem_deskitem')

        # Deleting model 'DeskItemLoan'
        db.delete_table(u'deskitem_deskitemloan')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'deskitem.deskitem': {
            'Meta': {'object_name': 'DeskItem'},
            'at_dorm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_loan_duration': ('timedelta.fields.TimedeltaField', [], {'default': 'None', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resident_set': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'desk_items'", 'symmetrical': 'False', 'through': u"orm['deskitem.DeskItemLoan']", 'to': u"orm['residents.Resident']"})
        },
        u'deskitem.deskitemloan': {
            'Meta': {'object_name': 'DeskItemLoan'},
            'desk_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'desk_item_loans'", 'to': u"orm['deskitem.DeskItem']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loaned_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'resident': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'desk_item_loans'", 'to': u"orm['residents.Resident']"}),
            'returned_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        u'residents.resident': {
            'Meta': {'object_name': 'Resident'},
            'dorm': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'STU'", 'max_length': '3'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['deskitem']