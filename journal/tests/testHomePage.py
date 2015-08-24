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
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_home_page_can_save_a_POST_request(self):
        response = self.client.post('/',{'entry_text':'A new journal entry'})

        self.assertEqual(JournalEntry.objects.count(),1)
        new_journal_entry = JournalEntry.objects.first()
        self.assertEqual(new_journal_entry.text, 'A new journal entry')
    
    def test_home_page_redirects_after_POST(self):
        response = self.client.post('/',{'entry_text':'A new journal entry'})
        self.assertRedirects(response, '/')

    def test_home_page_only_saves_items_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(JournalEntry.objects.count(), 0)

    def test_home_page_displays_all_journal_entries(self):
        JournalEntry.objects.create(text='journal entry 1')
        JournalEntry.objects.create(text='journal entry 2')

        response = self.client.get('/')

        self.assertContains(response,'journal entry 1')
        self.assertContains(response,'journal entry 2')

    def test_home_page_does_not_allow_to_enter_journal_entry_when_there_already_is_one_for_this_day(self):
        JournalEntry.objects.create(text='journal entry of today')

        response = self.client.get('/')

        self.assertNotContains(response,'id_new_journal_entry')
        self.assertNotContains(response,'id_submit_journal_entry')
