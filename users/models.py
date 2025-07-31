# from django.db import models
# from django.contrib.auth.models import User

# class LoginLocation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_locations')
#     ip_address = models.GenericIPAddressField()
#     city = models.CharField(max_length=100, blank=True)
#     region = models.CharField(max_length=100, blank=True)
#     country = models.CharField(max_length=100, blank=True)
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} from {self.city}, {self.region} ({self.ip_address})"
