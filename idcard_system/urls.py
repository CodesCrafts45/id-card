from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from cards import views as card_views
from notices import views as notice_views

admin.site.site_header = "আইডি কার্ড অ্যাডমিন প্যানেল"
admin.site.site_title = "ID Card Admin"
admin.site.index_title = "ড্যাশবোর্ড"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", card_views.home, name="home"),
    path("register/", card_views.register, name="register"),
    path("card/<uuid:uid>/", card_views.card_view, name="card_view"),
    path("card/<uuid:uid>/pdf/", card_views.card_pdf, name="card_pdf"),
    path("students/", card_views.student_list, name="student_list"),
    path("notices/", notice_views.notice_list, name="notice_list"),
    path("notices/<int:pk>/", notice_views.notice_detail, name="notice_detail"),
    path("notices/<int:pk>/pdf/", notice_views.notice_pdf, name="notice_pdf"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
