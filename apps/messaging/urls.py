from django.urls import path
from .views import detail, inbox
app_name = "messaging"
urlpatterns = [path("", inbox, name="inbox"), path("<int:pk>/", detail, name="detail")]
