from django.urls import path
from . import views


urlpatterns = [
    path('',views.index ,name="index"),
    path('add/',views.addcontact ,name="addcontact"),
    path('save/',views.save,name="save"),
    path('contact/<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('contact/<int:contact_id>/edit/', views.edit_contact, name='edit_contact'),
    path('contact/<int:contact_id>/delete/', views.delete_contact, name='delete_contact'),

]