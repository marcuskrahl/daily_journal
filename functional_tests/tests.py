from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from journal.tests.date_faker import DateFaker

class NewJournalEntryTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.date_faker = DateFaker()

    def tearDown(self):
        self.browser.quit()
        self.date_faker.reset()


    def get_entry_elements(self,subclass):
        return self.browser.find_elements_by_css_selector('p.entry '+subclass)

    def check_for_entry_text_in_entries(self, entry_text):
        entries = self.get_entry_elements('.entry-text')
        self.assertIn(entry_text, [entry.text for entry in entries])

    def check_for_entry_date_in_entries(self, entry_date):
        entries = self.get_entry_elements('.entry-date')
        self.assertIn(entry_date, [entry.text for entry in entries])

    def get_journal_entry_input(self):
        return self.browser.find_element_by_id('id_new_journal_entry')

    def get_journal_entry_send_button(self):
        return self.browser.find_element_by_id('id_submit_journal_entry')

    def write_journal_entry_for_date(self,entry_text,date):
        #It is the given date 
        self.date_faker.fake_date(date)

        # Anne wants to write a journal entry. She goes to the homepage
        self.browser.get(self.live_server_url)

        # She enters the journal entry
        inputbox = self.get_journal_entry_input()
        inputbox.send_keys(entry_text)

        # There is a button to submit the entry
        send_button = self.get_journal_entry_send_button()

        # When she sends the entry, the page updates and her entry is shown as commited
        send_button.click()
        self.check_for_entry_text_in_entries(entry_text)



    def test_can_write_daily_entry_and_retrieve_it_later(self): 
        # Anne wants to write her daily journal entry. She goes to the homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention the daily journal
        self.assertIn('Daily Journal', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Daily Journal', header_text)

        # She has the option to enter her journal entry
        inputbox = self.get_journal_entry_input()
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a new journal entry')

        # She types her journal entry
        inputbox.send_keys('This is my brand new diary entry')
        
        # There is a button to submit the entry
        send_button = self.get_journal_entry_send_button()
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

    def test_can_write_multiple_journal_entries(self):
        #Anne writes her first journal entry on the 15th of May 2015
        self.write_journal_entry_for_date('This is my first journal entry',date(2015,5,15))

        # She wants to add another entry, but she can't because she already wrote one for today
        with self.assertRaises(NoSuchElementException):
            self.get_journal_entry_input()
        with self.assertRaises(NoSuchElementException):
            self.get_journal_entry_send_button()

        # Anne is waiting another day to write a new journal entry.
        self.write_journal_entry_for_date('This is my second journal entry',date(2015,5,16))
        # The page is refreshing and showing the entries. 
        # The second entry is displayed on top, the first entry on bottom
        text_elements = self.get_entry_elements(".entry-text")
        date_elements = self.get_entry_elements(".entry-date") 

        self.assertEqual('This is my second journal entry',text_elements[0].text)
        self.assertEqual('This is my first journal entry',text_elements[1].text)

        self.assertEqual('2015-05-16',date_elements[0].text)
        self.assertEqual('2015-05-15',date_elements[1].text)

    def test_can_write_weekly_journal_entries(self):
        #Anne writes her first journal entry on the 15th of May 2015
        self.write_journal_entry_for_date('This is my first journal entry',date(2015,5,15))

        #She also wrote an entry 3 days later
        self.write_journal_entry_for_date('This is my second journal entry',date(2015,5,18))

        #A whole week has passed. It is time for a weekly journal entry.
        #When she visits the page, she is prompted to write a weekly journal entry
        self.date_faker.fake_date(date(2015,5,22))
        self.browser.get(self.live_server_url)

        #She is prompted to write a weekly journal entry
        weekly_entry_prompt = self.get_weekly_entry_prompt()
        self.assertIn('New weekly journal entry due', weekly_entry_prompt.text)

        #She confirms the prompt
        weekly_entry_prompt.click()

        #She is taken to a page where she can write her weekly journal entry
        self.assertIn('Weekly Entry', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Weekly Entry', header_text)
        
        #There is an input element where she can enter her weekly journal entry.
        inputbox = self.get_weekly_entry_input()
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a new weekly entry')

        #All previous journal entries are displayed to help her write the entry
        self.fail('finish test')

