from django.db import models
from django.contrib.auth.models import User
from shelf_life.models import Product  


class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)

class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']