from django.db import models

# Create your models here.
class ContactForm(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    company = models.CharField(max_length=128)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"