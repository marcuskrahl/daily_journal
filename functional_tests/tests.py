from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date

class NewJournalEntryTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def get_entry_elements(self,subclass):
        return self.browser.find_elements_by_css_selector('p.entry '+subclass)

    def check_for_entry_text_in_entries(self, entry_text):
        entries = self.get_entry_elements('.entry-text')
        self.assertIn(entry_text, [entry.text for entry in entries])

    def check_for_entry_date_in_entries(self, entry_date):
        entries = self.get_entry_elements('.entry-date')
        self.assertIn(entry_date, [entry.text for entry in entries])


    def test_can_write_daily_entry_and_retrieve_it_later(self): 
        # Anne wants to write her daily journal entry. She goes to the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the daily journal
        self.assertIn('Daily Journal', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Daily Journal', header_text)

        # She has the option to enter her journal entry
        inputbox = self.browser.find_element_by_id('id_new_journal_entry')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a new journal entry')

        # She types her journal entry
        inputbox.send_keys('This is my brand new diary entry')
        
        # There is a button to submit the entry
        send_button = self.browser.find_element_by_id('id_submit_journal_entry')
        self.assertEqual(send_button.get_attribute('value'),'Submit')

        # When she sends the entry, the page updates and her entry is shown as commited
        send_button.click()
        self.check_for_entry_text_in_entries('This is my brand new diary entry')
        
        #The entry displays the correct creation date
        correct_date = date.today().isoformat()
        self.check_for_entry_date_in_entries(correct_date)

        # She is refreshing the page, her entry is still there
        self.browser.get(self.live_server_url)
        self.check_for_entry_text_in_entries('This is my brand new diary entry')
