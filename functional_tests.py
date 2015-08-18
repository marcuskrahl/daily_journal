from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys

class NewJournalEntryTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_write_daily_entry_and_retrieve_it_later(self): 
        # Anne wants to write her daily journal entry. She goes to the homepage
        self.browser.get('http://localhost:8000')

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
        
        entries = self.browser.find_elements_by_css_selector('p.entry')
        self.assertIn('This is my brand new diary entry', [entry.text for entry in entries])
        
        # She is refreshing the page, her entry is still there
        self.browser.get('http://localhost:8000')

        entries = self.browser.find_elements_by_css_selector('p.entry')
        self.assertIn('This is my brand new diary entry', [entry.text for entry in entries])

        # Satisfied, she closes the browser
        self.fail("Finish test")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
