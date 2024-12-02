from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/<int:pk>/register/', views.register_event, name='register_event'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('registration/<int:pk>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('contact/', views.contact_view, name='contact'),
]