from django.db import models

class JournalEntry(models.Model):
    text = models.TextField(default='')
