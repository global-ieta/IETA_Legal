from django.urls import path
from .views import PAGES, home, page
app_name = "public"
urlpatterns = [path("", home, name="home")]
urlpatterns += [path("<slug:slug>/", page, name="page")]
