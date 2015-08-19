from django.shortcuts import render,redirect
from journal.models import JournalEntry

# Create your views here.
def home_page(request):
    if request.method == 'POST':
        JournalEntry.objects.create(text=request.POST['entry_text'])
        return redirect('/')

    journal_entries = JournalEntry.objects.all()
    return render(request, 'home.html', {'journal_entries': journal_entries})
