from django.urls import path
from .views import center, create_request, update_consent
app_name = "privacy"
urlpatterns = [path("", center, name="center"), path("consent/", update_consent, name="update_consent"), path("request/", create_request, name="create_request")]
