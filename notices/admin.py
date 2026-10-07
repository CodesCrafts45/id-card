from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at", "updated_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_per_page = 20
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("📢 নোটিশ", {
            "fields": ("title", "content", "is_published"),
        }),
        ("📎 মিডিয়া", {
            "fields": ("image", "pdf_file"),
            "description": "ছবি ও PDF ফাইল আপলোড করুন",
        }),
    )
