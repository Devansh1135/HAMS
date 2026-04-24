from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ("patient","Patient"),
        ("doctor","Doctor")
    ]
    name = models.CharField(choices=ROLE_CHOICES,max_length=10)