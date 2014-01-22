# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "desk_permission_fixture.json")

    def backwards(self, orm):
        raise NotImplementedError

    models = {
    }

    complete_apps = ['desk']
    symmetrical = True
