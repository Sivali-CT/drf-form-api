from django.urls import path
from .views import ContactMessageCreateView, ContactFormListView

urlpatterns = [
    path('create/', ContactMessageCreateView.as_view(), name='contact-message-create'),
    path('list/', ContactFormListView.as_view(), name='contact-form-list'),

]