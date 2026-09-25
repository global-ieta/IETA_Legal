from django.urls import path
from .views import decide, list_consultations
app_name = "consultations"
urlpatterns = [path("", list_consultations, name="list"), path("<int:pk>/<str:decision>/", decide, name="decide")]
