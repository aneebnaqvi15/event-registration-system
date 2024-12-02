from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from .models import Event, Registration

def event_list(request):
    # Get all events and order them by date
    events_list = Event.objects.all().order_by('date')
    
    # Add pagination
    paginator = Paginator(events_list, 9)  # Show 9 events per page
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    # Get event or return 404
    event = get_object_or_404(Event, pk=pk)
    
    # Check if user is already registered
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(
            user=request.user, 
            event=event
        ).exists()
    
    context = {
        'event': event,
        'is_registered': is_registered
    }
    return render(request, 'events/event_detail.html', context)

@login_required
def register_event(request, pk):
    if request.method != 'POST':
        return redirect('event_detail', pk=pk)
    
    event = get_object_or_404(Event, pk=pk)
    
    # Check if event is full
    if event.spots_remaining < 1:
        messages.error(request, 'Sorry, this event is full.')
        return redirect('event_detail', pk=pk)
    
    try:
        # Attempt to create registration
        Registration.objects.create(user=request.user, event=event)
        messages.success(request, 'Successfully registered for the event!')
    except IntegrityError:
        # Handle case where user is already registered
        messages.warning(request, 'You are already registered for this event.')
    
    return redirect('event_detail', pk=pk)

@login_required
def my_registrations(request):
    # Get user's registrations
    registrations = Registration.objects.filter(
        user=request.user
    ).select_related('event').order_by('event__date')
    
    return render(request, 'events/my_registrations.html', 
                 {'registrations': registrations})

@login_required
def cancel_registration(request, pk):
    if request.method != 'POST':
        return redirect('my_registrations')
    
    registration = get_object_or_404(Registration, 
                                   pk=pk, 
                                   user=request.user)
    registration.delete()
    messages.success(request, 'Registration cancelled successfully.')
    return redirect('my_registrations') 