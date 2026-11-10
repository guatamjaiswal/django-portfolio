from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact
from .forms import ContactForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')    
def about(request):
    return render(request, 'about.html')
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, 'contact.html', {
                'form': ContactForm(),
                'success': 'Your message has been sent successfully!'
            })

    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form
    })
    
@login_required    
def dashboard(request):
    search_query = request.GET.get('search', '').strip()

    contacts = Contact.objects.all()

    if search_query:
        contacts = contacts.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    total_contacts = Contact.objects.count()
    new_contacts = Contact.objects.filter(status='new').count()
    read_contacts = Contact.objects.filter(status='read').count()
    replied_contacts = Contact.objects.filter(status='replied').count()

    contacts = contacts.order_by('-created_at')

    paginator = Paginator(contacts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_contacts': total_contacts,
        'new_contacts': new_contacts,
        'read_contacts': read_contacts,
        'replied_contacts': replied_contacts,
        'recent_contacts': page_obj.object_list,
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'dashboard.html', context)

@login_required
def view_message(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        new_status = request.POST.get('status')

        valid_statuses = ['new', 'read', 'replied']

        if new_status in valid_statuses:
            contact.status = new_status
            contact.save(update_fields=['status'])

    return render(request, 'view_message.html', {
        'contact': contact
    })

@login_required
def delete_contact(request, contact_id):
    if request.method == "POST":
        contact = get_object_or_404(Contact, id=contact_id)
        contact.delete()

    return redirect('dashboard')
   
@login_required 
def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            return redirect('dashboard')

    else:
        form = ContactForm(instance=contact)

    return render(request, 'edit_contact.html', {
        'form': form,
        'contact': contact
    })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    