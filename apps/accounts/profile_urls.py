from django.urls import path
from .views import profile

app_name = "accounts_profile"
urlpatterns = [path("", profile, name="profile")]
