from journal.models import JournalEntry

class DateFaker():
    
    original_get_date = None

    def fake_date(self,faked_date):
        if self.original_get_date is None:
            self.original_get_date = JournalEntry.get_entry_date
        JournalEntry.get_entry_date = lambda: faked_date

    def reset(self):
        JournalEntry.get_entry_date = self.original_get_date
        self.original_get_date = None
    
    
