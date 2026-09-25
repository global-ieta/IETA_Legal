from django.urls import path
from .views import detail, list_matters
app_name = "matters"
urlpatterns = [path("", list_matters, name="list"), path("<int:pk>/", detail, name="detail")]
