from django.contrib import admin
from .models import EventSettings, DeveloperCard


@admin.register(EventSettings)
class EventSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("🏛️ ইভেন্ট / প্রতিষ্ঠান", {
            "fields": ("event_name", "institution_address", "logo"),
            "classes": ("wide",),
        }),
        ("🎨 ব্যাকগ্রাউন্ড ও কালার", {
            "fields": (
                "background_image", "background_color",
                ("gradient_start", "gradient_end"),
                ("card_primary_color", "card_secondary_color"),
                "text_color",
            ),
            "classes": ("wide",),
            "description": "সাইট ও আইডি কার্ডের রং নিয়ন্ত্রণ করুন",
        }),
        ("👁️ কোন ফিল্ড দেখাবে (আইডি কার্ডে)", {
            "fields": (
                ("show_name", "show_class", "show_roll"),
                ("show_designation", "show_blood_group", "show_address"),
                ("show_phone", "show_email", "show_profile_pic", "show_qr"),
            ),
            "classes": ("wide",),
        }),
    )

    def has_add_permission(self, request):
        return not EventSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# DeveloperCard — অ্যাডমিন থেকে পরিবর্তন করা যাবে না
# শুধু কোড/ডাটাবেস থেকে সেট করা যাবে
class DeveloperCardAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False  # সাইডবারে দেখাবে না

    def has_view_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# Register but fully locked
admin.site.register(DeveloperCard, DeveloperCardAdmin)
