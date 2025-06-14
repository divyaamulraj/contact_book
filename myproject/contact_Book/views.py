from django.shortcuts import render,redirect
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Contact
from django.shortcuts import get_object_or_404
from .forms import ContactForm
from django.contrib import messages

def index(request):
    query = request.GET.get('q', '').strip()  # get the search term from the URL

    if query:
        # First get contacts that match the search query
        matched_contacts = Contact.objects.filter(name__icontains=query)
        # Then get the rest of the contacts (excluding already matched)
        unmatched_contacts = Contact.objects.exclude(name__icontains=query)
        # Combine both, with matched ones at the top
        contacts = list(matched_contacts) + list(unmatched_contacts)
    else:
        # If no query, show all normally
        contacts = Contact.objects.all()

    return render(request, 'index.html', {
        'contacts': contacts,
        'query': query,
    })
# def index(request):
    # contacts = Contact.objects.all()  
    # return render(request, 'index.html', {'contacts': contacts})
def addcontact(request):
    return render(request,'addcontact.html')
# def save(request):
#     if request.method == 'POST':
#         # get data from form
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         email = request.POST.get('email')
#         # save to DB using model
#         Contact.objects.create(name=name, phone=phone, city=city, state=state, email=email)
#         return redirect('addcontact')
#     return render(request, 'addcontact.html')
def save(request):
    if request.method == 'POST':
        # get data from form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        email = request.POST.get('email')
        
        # check for duplicate contact
        if Contact.objects.filter(name=name, phone=phone, city=city, state=state, email=email).exists():
            # optional: show a message
            # messages.error(request, "This contact already exists.")
            return redirect('addcontact')  # just do nothing if duplicate

        # save new contact if it's unique
        Contact.objects.create(name=name, phone=phone, city=city, state=state, email=email)
        return redirect('addcontact')

    return render(request, 'addcontact.html')
def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'contact_detail.html', {'contact': contact})


def edit_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            # Check for duplicate contacts
            cleaned_data = form.cleaned_data
            if Contact.objects.exclude(id=contact_id).filter(
                name=cleaned_data['name'],
                phone=cleaned_data['phone'],
                email=cleaned_data['email'],
                city=cleaned_data['city'],
                state=cleaned_data['state'],
            ).exists():
                # Do not save, just ignore or show nothing
                return redirect('index')  # or stay on the edit page
            form.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'edit_contact.html', {'form': form, 'contact': contact})
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if request.method == 'POST':
        contact.delete()
        return redirect('index')  # after deletion, redirect to contact list
    return redirect('contact_detail', contact_id=contact.id)
