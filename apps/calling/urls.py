from django.urls import path
from .views import lobby, status
app_name = "calling"
urlpatterns = [path("status/", status, name="status"), path("<int:consultation_id>/<str:mode>/", lobby, name="lobby")]
