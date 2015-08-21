# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import journal.models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_journalentry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='date',
            field=models.DateField(default=journal.models.JournalEntry.get_entry_wrapper),
        ),
    ]
