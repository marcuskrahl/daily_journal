# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_journalentry_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='date',
            field=models.DateField(default=datetime.date(2015, 8, 21)),
            preserve_default=False,
        ),
    ]
