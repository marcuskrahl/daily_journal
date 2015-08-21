from datetime import date
from django.db import models

class JournalEntry(models.Model):
    @staticmethod
    def get_entry_date():
        return date.today()

    def get_entry_wrapper():
        return JournalEntry.get_entry_date()
    
    text = models.TextField(default='')
    date = models.DateField(default=get_entry_wrapper)

