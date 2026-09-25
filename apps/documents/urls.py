from django.urls import path
from .views import download, library, upload
app_name = "documents"
urlpatterns = [path("", library, name="library"), path("upload/", upload, name="upload"), path("<int:pk>/download/", download, name="download")]
