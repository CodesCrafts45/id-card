from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from .models import Notice
from core.models import EventSettings
import os


def notice_list(request):
    settings = EventSettings.get_solo()
    notices = Notice.objects.filter(is_published=True)
    return render(request, "notices/list.html", {"notices": notices, "settings": settings})


def notice_detail(request, pk):
    settings = EventSettings.get_solo()
    notice = get_object_or_404(Notice, pk=pk, is_published=True)
    return render(request, "notices/detail.html", {"notice": notice, "settings": settings})


def notice_pdf(request, pk):
    notice = get_object_or_404(Notice, pk=pk, is_published=True)
    if not notice.pdf_file:
        raise Http404("PDF পাওয়া যায়নি")

    try:
        notice.pdf_file.open("rb")
        return FileResponse(
            notice.pdf_file,
            as_attachment=True,
            filename=os.path.basename(notice.pdf_file.name),
        )
    except Exception as exc:
        raise Http404("PDF পাওয়া যায়নি") from exc
