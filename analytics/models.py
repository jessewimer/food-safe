from django.db import models

class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)
