from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
PAGES = {
    "about": ("About IETA Legal", "IETA Legal is a connected information and advocate-communication layer within the Global IETA ecosystem."),
    "how-it-works": ("How it works", "Describe facts, review your information, explore independently verified advocates, and choose your next conversation yourself."),
    "for-users": ("For users", "A guided place to organise what happened, preserve your own context, and prepare for a conversation with an advocate."),
    "for-advocates": ("For advocates", "A professional workspace for independently verified advocates to receive authorised matter context and communicate with users."),
    "aura": ("AURA", "AURA is an information-gathering clerk. It can ask factual questions and organise user-provided information; it is not a lawyer and does not give legal advice."),
    "consultations": ("Consultations", "Consultations are conversations between a user and an independent advocate. IETA Legal does not provide representation or guarantee outcomes."),
    "privacy": ("Privacy", "Privacy is designed around data minimisation, explicit consent, access boundaries, and an owner-replaceable storage layer."),
    "terms": ("Terms", "These product terms describe the service, its boundaries, and the responsibilities of platform participants."),
    "legal-disclaimer": ("Legal disclaimer", "IETA Legal is a technology platform, not a law firm. Platform information is not legal advice."),
    "advocate-disclaimer": ("Advocate disclaimer", "Advocates remain independent professionals. Profiles and availability should be independently evaluated by users."),
    "faq": ("Questions, answered", "Learn what the platform does, what AURA does, how advocates are selected, and how account access works."),
    "contact": ("Contact", "Contact and service arrangements will be connected to Global IETA infrastructure after the official contract is supplied."),
}
def home(request): return render(request, "public/home.html", {"meta_description": "IETA Legal helps people organise factual information and connect with independently verified advocates."})
def page(request, slug):
    title, intro = PAGES[slug]
    return render(request, "public/content_page.html", {"page_title": title, "page_intro": intro, "meta_description": intro, "slug": slug})

def sitemap(request):
    paths = [reverse("public:home"), reverse("advocates:directory")]
    paths += [reverse("public:page", kwargs={"slug": slug}) for slug in PAGES]
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(f"<url><loc>{request.build_absolute_uri(path)}</loc></url>" for path in paths) + "</urlset>"
    return HttpResponse(body, content_type="application/xml")

def robots(request):
    body = "User-agent: *\nAllow: /\nDisallow: /portal/\nDisallow: /development/\nDisallow: /intake/\nDisallow: /aura/\nDisallow: /messages/\nDisallow: /documents/\nDisallow: /notifications/\nDisallow: /admin-portal/\nSitemap: " + request.build_absolute_uri(reverse("sitemap")) + "\n"
    return HttpResponse(body, content_type="text/plain")

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)
