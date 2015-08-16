from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')
        
        # She has the option to enter her journal entry
        
        # She types her journal entry
        
        # When she confirms the entry, the page updates and her entry is shown as commited
        
        # She is refreshing the page, her entry is still there

        # Satisfied, she closes the browser

if __name__ == '__main__':
    unittest.main(warnings='ignore')
