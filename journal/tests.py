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

        self.assertEqual(JournalEntry.objects.count(),1)
        new_journal_entry = JournalEntry.objects.first()
        self.assertEqual(new_journal_entry.text, 'A new journal entry')
    
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST["entry_text"] = "A new journal entry"

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(JournalEntry.objects.count(), 0)

    def test_home_page_displays_all_journal_entries(self):
        JournalEntry.objects.create(text='journal entry 1')
        JournalEntry.objects.create(text='journal entry 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('journal entry 1',response.content.decode())
        self.assertIn('journal entry 2',response.content.decode())

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
