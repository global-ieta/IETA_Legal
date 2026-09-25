from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import get_valid_filename
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from apps.core.rate_limit import apply_rate_limit_headers, check_request
from apps.matters.models import Matter
from apps.core.integration_readiness import get_integration_readiness
from integrations.documents.exceptions import DocumentSafetyIntegrationUnavailable
from integrations.documents.services import get_document_safety_provider
from integrations.storage.services import get_private_storage_provider
from .forms import PrivateDocumentForm
from .models import PrivateDocument
from .services import can_access_document

def _accessible_matters(request):
    if request.demo_role == "USER":
        return Matter.objects.filter(owner_id=request.demo_user_id)
    if request.demo_role == "ADVOCATE":
        return Matter.objects.filter(selected_advocate__user_id=request.demo_user_id)
    return Matter.objects.all()

def library(request):
    if not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}):
        return redirect("auth_login")
    matter_id = request.GET.get("matter_id")
    matters = _accessible_matters(request)
    documents = PrivateDocument.objects.select_related("matter", "uploaded_by").filter(matter__in=matters)
    if matter_id:
        documents = documents.filter(matter_id=matter_id)
    return render(request, "portal/documents.html", {"documents": documents, "matters": matters, "selected_matter": matter_id})

def upload(request):
    if not require_demo_role(request, {"USER", "ADVOCATE"}):
        return redirect("auth_login")
    matter = get_object_or_404(_accessible_matters(request), pk=request.GET.get("matter_id") or request.POST.get("matter_id"))
    if request.method == "POST":
        rate_limit = check_request(request, "documents")
        if not rate_limit.allowed:
            messages.error(request, "Document uploads are temporarily limited. Please wait before trying again.")
            record_event(request, "document.rate_limited", matter, {"bucket": "documents", "limit": rate_limit.limit})
            response = render(request, "portal/document_upload.html", {"form": PrivateDocumentForm(), "matter": matter}, status=429)
            return apply_rate_limit_headers(response, rate_limit)
        form = PrivateDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.cleaned_data["file"]
            if not get_private_storage_provider().status().operational:
                messages.error(request, "Private document storage is not configured yet; the upload was not stored.")
                return render(request, "portal/document_upload.html", {"form": form, "matter": matter}, status=503)
            try:
                scan_result = get_document_safety_provider().scan(
                    file_name=get_valid_filename(upload_file.name)[:255],
                    content_type=getattr(upload_file, "content_type", ""),
                    size=upload_file.size,
                )
            except DocumentSafetyIntegrationUnavailable:
                messages.error(request, "Document scanning is not configured yet; the upload was not stored.")
                return render(request, "portal/document_upload.html", {"form": form, "matter": matter}, status=503)
            document = PrivateDocument.objects.create(matter=matter, uploaded_by_id=request.demo_user_id, file=upload_file, original_name=get_valid_filename(upload_file.name)[:255], content_type=getattr(upload_file, "content_type", ""), size=upload_file.size)
            record_event(request, "document.uploaded", document, {"size": upload_file.size, "status": document.status, "scanner_status": scan_result.status, "automated_scan": scan_result.metadata.get("automated_scan", False)})
            messages.success(request, "The document was stored privately and queued for security review.")
            return redirect(f"/documents/?matter_id={matter.pk}")
    else:
        form = PrivateDocumentForm()
    return render(request, "portal/document_upload.html", {"form": form, "matter": matter})

def download(request, pk):
    if not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}):
        raise Http404
    document = get_object_or_404(PrivateDocument, pk=pk)
    if not can_access_document(document, request.demo_user_id, request.demo_role) or document.status != PrivateDocument.Status.AVAILABLE:
        raise Http404
    record_event(request, "document.downloaded", document, {"status": document.status})
    return FileResponse(document.file.open("rb"), as_attachment=True, filename=document.original_name)
