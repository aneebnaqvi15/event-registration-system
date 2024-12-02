from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Event, Registration
from .forms import UserRegistrationForm



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('event_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

def event_list(request):
    events = Event.objects.all().order_by('date')
    context = {
        'events': events,
        'show_checkout': True  # i add this to control checkout button visibility
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = request.user.is_authenticated and Registration.objects.filter(
        user=request.user, 
        event=event
    ).exists()
    context = {
        'event': event,
        'is_registered': is_registered,
        'show_checkout': True  #  this is  to control checkout button visibility
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user is already registered
    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('event_detail', pk=pk)
    
    if event.spots_remaining < 1:
        messages.error(request, 'Sorry, this event is full.')
        return redirect('event_detail', pk=pk)
    
    Registration.objects.create(user=request.user, event=event)
    messages.success(request, 'Successfully registered for the event!')
    return redirect('event_detail', pk=pk)

@login_required
def my_registrations(request):
    registrations = Registration.objects.filter(user=request.user).order_by('event__date')
    context = {
        'registrations': registrations,
        'show_checkout': True  #  this is add to control checkout button visibility
    }
    return render(request, 'events/my_registrations.html', context)

@login_required
def cancel_registration(request, pk):
    if request.method != 'POST':
        return redirect('my_registrations')
    
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    event_title = registration.event.title  # Store event title before deletion
    registration.delete()
    messages.success(request, f'Registration for "{event_title}" cancelled successfully.')
    return redirect('my_registrations')

def contact_view(request):
    return render(request, 'events/contact.html')