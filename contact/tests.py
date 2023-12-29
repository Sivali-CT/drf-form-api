from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import ContactForm

class ContactFormTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact_data = {
            'first_name': 'Andini',
            'last_name': 'Anissa',
            'company': 'Test',
            'email': 'andin@test.co.id',
            'message': 'Hi, there! This is a test message.'
        }

    def test_create_contact_form(self):
        response = self.client.post('/api/contact/create/', self.contact_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactForm.objects.count(), 1)


        contact_form = ContactForm.objects.get()
        self.assertEqual(contact_form.first_name, self.contact_data['first_name'])
        self.assertEqual(contact_form.last_name, self.contact_data['last_name'])
        self.assertEqual(contact_form.company, self.contact_data['company'])
        self.assertEqual(contact_form.email, self.contact_data['email'])
        self.assertEqual(contact_form.message, self.contact_data['message'])

    def test_invalid_contact_form(self):
        invalid_data = {'first_name': 'Andini'}
        response = self.client.post('/api/contact/create/', invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ContactForm.objects.count(), 0)