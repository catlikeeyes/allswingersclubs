# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("CREATE USER IF NOT EXISTS 'fetlife-79d0d24e487711e7a919'@'localhost' IDENTIFIED BY '_Wyhr6*?6aJYAqtNb9w2qM+F96UaEE';")
        db.execute("CREATE USER IF NOT EXISTS 'fetlife-79d0d24e487711e7a919'@'%' IDENTIFIED BY '_Wyhr6*?6aJYAqtNb9w2qM+F96UaEE';")
        db.execute("GRANT ALL ON fetlife.* TO 'fetlife-79d0d24e487711e7a919'@'localhost';")
        db.execute("GRANT ALL ON fetlife.* TO 'fetlife-79d0d24e487711e7a919'@'%';")
        db.execute("FLUSH PRIVILEGES;")


    def backwards(self, orm):
        pass

    models = {
        'forum.group': {
            'Meta': {'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orig_group_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'forum.grouppost': {
            'Meta': {'object_name': 'GroupPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orig_post_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'forum.grouppostcomment': {
            'Meta': {'object_name': 'GroupPostComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'group_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.GroupPost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'forum.postauthor': {
            'Meta': {'object_name': 'PostAuthor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'orig_user_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'})
        },
        'forum.userblogpost': {
            'Meta': {'object_name': 'UserBlogPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'forum.userblogpostcomment': {
            'Meta': {'object_name': 'UserBlogPostComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.PostAuthor']"}),
            'blog_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.UserBlogPost']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['forum']
    symmetrical = True
