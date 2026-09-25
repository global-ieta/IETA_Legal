from django.urls import path
from .views import directory, profile, request_consultation
app_name = "advocates"
urlpatterns = [path("", directory, name="directory"), path("<int:pk>/", profile, name="profile"), path("<int:pk>/request/", request_consultation, name="request_consultation")]
