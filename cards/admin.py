from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "class_name", "roll", "designation", "blood_group", "phone", "is_active", "created_at")
    list_filter = ("class_name", "blood_group", "is_active", "created_at")
    search_fields = ("name", "roll", "phone", "email", "designation")
    readonly_fields = ("unique_id", "created_at", "updated_at")
    list_editable = ("is_active",)
    list_per_page = 25
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        ("👤 মূল তথ্য", {
            "fields": ("name", ("class_name", "roll"), "designation", "blood_group"),
        }),
        ("📞 যোগাযোগ", {
            "fields": (("phone", "email"), "address"),
        }),
        ("🖼️ ছবি ও স্ট্যাটাস", {
            "fields": ("profile_picture", "is_active"),
        }),
        ("🔑 সিস্টেম তথ্য", {
            "fields": ("unique_id", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
