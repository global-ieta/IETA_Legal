from django.urls import path
from .views import audit_log, documents, integration_status, privacy_requests, review_document, review_privacy_request

app_name = "admin_portal"
urlpatterns = [
    path("", documents, name="documents"),
    path("documents/<int:pk>/<str:decision>/", review_document, name="review_document"),
    path("audit/", audit_log, name="audit_log"),
    path("integrations/", integration_status, name="integration_status"),
    path("privacy/", privacy_requests, name="privacy_requests"),
    path("privacy/<int:pk>/<str:decision>/", review_privacy_request, name="review_privacy_request"),
]
