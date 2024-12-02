# contacts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, ContactForm
from .models import Contact
from django.contrib.auth.decorators import login_required

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log the user in immediately after registration
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, '/register.html', {'form': form})

# User Login View (Using Django's built-in form)
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, '/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Index View for displaying contacts
@login_required
def index(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'contacts/index.html', {'contacts': contacts})

# Add Contact View
@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # Associate the contact with the current user
            contact.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, '/add_contact.html', {'form': form})

