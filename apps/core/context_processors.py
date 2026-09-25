from django.conf import settings

def site_context(request):
    private_prefixes = ("/portal/", "/development/", "/intake/", "/aura/", "/messages/", "/documents/", "/notifications/", "/admin-portal/", "/admin/")
    is_private = request.path.startswith(private_prefixes)
    display_name = request.session.get("demo_display_name")
    if not display_name and request.user.is_authenticated:
        display_name = request.user.get_full_name() or request.user.get_username()
    return {"demo_mode": settings.DEMO_MODE, "demo_role": getattr(request, "demo_role", None), "display_name": display_name, "brand_name": "IETA Legal", "canonical_url": request.build_absolute_uri(request.path), "robots_directive": "noindex, nofollow" if is_private else "index, follow"}
