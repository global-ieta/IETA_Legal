from django.urls import path
from .views import message, workspace
app_name = "aura"
urlpatterns = [path("", workspace, name="workspace"), path("message/", message, name="message")]
