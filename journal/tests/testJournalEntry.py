from django.test import TestCase
from journal.models import JournalEntry
from datetime import date,timedelta
from journal.tests.date_faker import DateFaker

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

    def test_new_journal_entry_defaults_to_today(self):
        entry = JournalEntry()
        entry.save()

        entry = JournalEntry.objects.all()[0]

        self.assertEqual(entry.date,date.today())

    def test_creating_journal_entry_checks_for_date(self):
        date_faker = DateFaker()
        try:
            date_faker.fake_date(date(2015,3,15))
            entry = JournalEntry()
            entry.save()

            saved_journal_entries = JournalEntry.objects.all()
            self.assertEqual(saved_journal_entries.count(),1)

            entry = saved_journal_entries[0]
            self.assertEqual(entry.date,date(2015,3,15))
        finally:
            date_faker.reset()

