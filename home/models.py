from django.db import models

# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(
    max_length=10,
    choices=[
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ],
    default='new'
)
    def __str__(self):
        return self.name
    

    