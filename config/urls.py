from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from apps.accounts.views import login_view, logout_view, register, register_advocate
from apps.public_site.views import robots, sitemap

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="auth_login"),
    path("register/", register, name="auth_register"),
    path("register/advocate/", register_advocate, name="auth_register_advocate"),
    path("logout/", logout_view, name="auth_logout"),
    path("forgot-password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html", email_template_name="accounts/password_reset_email.txt", success_url=reverse_lazy("auth_password_reset_done")), name="auth_password_reset"),
    path("forgot-password/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="auth_password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html", success_url=reverse_lazy("auth_password_reset_complete")), name="auth_password_reset_confirm"),
    path("reset/complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="auth_password_reset_complete"),
    path("development/", include("apps.accounts.urls")),
    path("profile/", include("apps.accounts.profile_urls")),
    path("portal/", include("apps.dashboard.urls")),
    path("intake/", include("apps.intake.urls")),
    path("aura/", include("apps.aura.urls")),
    path("advocates/", include("apps.advocates.urls")),
    path("matters/", include("apps.matters.urls")),
    path("consultations/", include("apps.consultations.urls")),
    path("messages/", include("apps.messaging.urls")),
    path("calls/", include("apps.calling.urls")),
    path("privacy/", include("apps.privacy.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("documents/", include("apps.documents.urls")),
    path("admin-portal/", include("apps.admin_portal.urls")),
    path("health/", include("apps.core.urls")),
    path("sitemap.xml", sitemap, name="sitemap"),
    path("robots.txt", robots, name="robots"),
    path("", include("apps.public_site.urls")),
]

handler404 = "apps.public_site.views.error_404"
handler500 = "apps.public_site.views.error_500"
