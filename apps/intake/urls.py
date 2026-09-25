from django.urls import path
from .views import confirm, edit, review, start
app_name = "intake"
urlpatterns = [path("start/", start, name="start"), path("<int:pk>/edit/", edit, name="edit"), path("<int:pk>/review/", review, name="review"), path("<int:pk>/confirm/", confirm, name="confirm")]
