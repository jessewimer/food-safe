# from django.urls import path
# from django.contrib.auth.views import LoginView

# urlpatterns = [
#     path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
# ]
# from django.urls import path
# from django.contrib.auth.views import LoginView
# from django.urls import reverse_lazy

# urlpatterns = [
#     path("login/", LoginView.as_view(
#         template_name="users/login.html",
#         success_url="/login/?login=success"  # Redirect back to login page with success param
#     ), name="login"),
# ]
from django.urls import path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="users/login.html",
        success_url="/?first_login=true"
    ), name="login"),
]