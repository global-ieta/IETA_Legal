from django.urls import path
from .views import entry, exit_demo
app_name = "accounts"
urlpatterns = [path("", entry, name="entry"), path("exit/", exit_demo, name="exit")]
