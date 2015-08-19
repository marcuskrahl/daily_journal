from django.core.urlresolvers import resolve
from django.test import TestCase
from journal.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from journal.models import JournalEntry

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(),expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["entry_text"] = "A new journal entry"

        response = home_page(request)
        self.assertIn('A new journal entry',response.content.decode())
        expected_html = render_to_string('home.html', {'journal_entry_text': 'A new journal entry'})
        self.assertEqual(response.content.decode(), expected_html)

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
