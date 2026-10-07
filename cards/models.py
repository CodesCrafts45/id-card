from django.db import models
import uuid


BLOOD_GROUP_CHOICES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]


class Student(models.Model):
    """রেজিস্ট্রেশন / স্টুডেন্ট তথ্য"""
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=150, verbose_name="নাম")
    class_name = models.CharField(max_length=50, verbose_name="ক্লাস", blank=True)
    roll = models.CharField(max_length=30, verbose_name="রোল", blank=True)
    designation = models.CharField(max_length=100, verbose_name="পদবি", blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True, verbose_name="ব্লাড গ্রুপ")
    address = models.TextField(verbose_name="ঠিকানা", blank=True)
    phone = models.CharField(max_length=20, verbose_name="ফোন", blank=True)
    email = models.EmailField(verbose_name="ইমেইল", blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True, verbose_name="প্রোফাইল পিকচার")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")

    class Meta:
        verbose_name = "স্টুডেন্ট / মেম্বার"
        verbose_name_plural = "স্টুডেন্ট / মেম্বারগণ"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.roll or self.unique_id.hex[:8]})"

    def get_qr_data(self):
        return f"ID:{self.unique_id}|Name:{self.name}|Class:{self.class_name}|Roll:{self.roll}|Phone:{self.phone}"

