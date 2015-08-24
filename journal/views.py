from django.shortcuts import render,redirect
from journal.models import JournalEntry
from datetime import date

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        JournalEntry.objects.create(text=request.POST['entry_text'])
        return redirect('/')

    journal_entries = JournalEntry.objects.all()
    no_entry_for_today = not JournalEntry.objects.filter(date=JournalEntry.get_entry_date()).exists()
    return render(request, 'home.html', {
        'journal_entries': journal_entries,
        'no_entry_for_today': no_entry_for_today
    })
