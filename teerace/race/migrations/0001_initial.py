# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Map'
        db.create_table('race_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('added_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('map_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('crc', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('map_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['race.MapType'])),
            ('has_unhookables', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_deathtiles', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shield_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('heart_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('grenade_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('has_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('download_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('race', ['Map'])

        # Adding model 'MapType'
        db.create_table('race_maptype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=20, db_index=True)),
            ('displayed_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('race', ['MapType'])

        # Adding model 'Run'
        db.create_table('race_run', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['race.Map'])),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(related_name='runs', to=orm['race.Server'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('checkpoints', self.gf('django.db.models.fields.CharField')(max_length=349, blank=True)),
            ('time', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_personal_best', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('was_personal_best', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_record', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('was_record', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('diff_from_personal_best', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('race', ['Run'])

        # Adding model 'BestRun'
        db.create_table('race_bestrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['race.Map'])),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['race.Run'])),
            ('time', self.gf('django.db.models.fields.FloatField')()),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('race', ['BestRun'])

        # Adding unique constraint on 'BestRun', fields ['user', 'map']
        db.create_unique('race_bestrun', ['user_id', 'map_id'])

        # Adding model 'Server'
        db.create_table('race_server', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('maintained_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maintained_servers', to=orm['auth.User'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_connection_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('played_map', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['race.Map'], null=True, blank=True)),
            ('anonymous_players', self.gf('picklefield.fields.PickledObjectField')()),
            ('api_key', self.gf('django.db.models.fields.CharField')(default='yzxnV3E4cY77963q693jADbQpRvNU2g5', unique=True, max_length=32)),
        ))
        db.send_create_signal('race', ['Server'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'BestRun', fields ['user', 'map']
        db.delete_unique('race_bestrun', ['user_id', 'map_id'])

        # Deleting model 'Map'
        db.delete_table('race_map')

        # Deleting model 'MapType'
        db.delete_table('race_maptype')

        # Deleting model 'Run'
        db.delete_table('race_run')

        # Deleting model 'BestRun'
        db.delete_table('race_bestrun')

        # Deleting model 'Server'
        db.delete_table('race_server')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'race.bestrun': {
            'Meta': {'unique_together': "(('user', 'map'),)", 'object_name': 'BestRun'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['race.Map']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['race.Run']"}),
            'time': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'race.map': {
            'Meta': {'object_name': 'Map'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'crc': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'grenade_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'has_deathtiles': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_unhookables': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'heart_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'map_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['race.MapType']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'shield_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'race.maptype': {
            'Meta': {'object_name': 'MapType'},
            'displayed_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '20', 'db_index': 'True'})
        },
        'race.run': {
            'Meta': {'object_name': 'Run'},
            'checkpoints': ('django.db.models.fields.CharField', [], {'max_length': '349', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diff_from_personal_best': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_personal_best': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_record': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['race.Map']"}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'runs'", 'to': "orm['race.Server']"}),
            'time': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'was_personal_best': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'was_record': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'race.server': {
            'Meta': {'object_name': 'Server'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'anonymous_players': ('picklefield.fields.PickledObjectField', [], {}),
            'api_key': ('django.db.models.fields.CharField', [], {'default': "'cHRBAmfCHxsb9PX9zxcssnh2sPQQVy2N'", 'unique': 'True', 'max_length': '32'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_connection_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'maintained_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maintained_servers'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'played_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['race.Map']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['race']
