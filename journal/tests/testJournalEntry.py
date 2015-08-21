from django.test import TestCase
from journal.models import JournalEntry

class JournalEntryModelTest(TestCase):

    def test_saving_and_retrieving_journal_entries(self):
        first_journal_entry = JournalEntry()
        first_journal_entry.text = 'The first (ever) journal entry'
        first_journal_entry.save()

        second_journal_entry = JournalEntry()
        second_journal_entry.text = 'Second journal entry'
        second_journal_entry.save()

        saved_journal_entries = JournalEntry.objects.all()
        self.assertEqual(saved_journal_entries.count(),2)

        first_journal_entry = saved_journal_entries[0]
        second_journal_entry = saved_journal_entries[1]
        self.assertEqual(first_journal_entry.text,'The first (ever) journal entry')
        self.assertEqual(second_journal_entry.text,'Second journal entry')
