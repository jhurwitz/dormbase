# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    depends_on = (
        ('guardian', '0005_auto__chg_field_groupobjectpermission_object_pk__chg_field_userobjectp'),
    )

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "deskworker_group_permission_fixture.json")

    def backwards(self, orm):
        raise NotImplementedError

    models = {
    }

    complete_apps = ['sampledorm']
    symmetrical = True
