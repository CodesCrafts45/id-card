from django.db import models


class EventSettings(models.Model):
    """ইভেন্ট / প্রতিষ্ঠানের সেটিংস - অ্যাডমিন থেকে পরিবর্তনযোগ্য"""
    event_name = models.CharField(max_length=200, verbose_name="ইভেন্ট / প্রতিষ্ঠানের নাম", default="আইডি কার্ড সিস্টেম")
    institution_address = models.TextField(verbose_name="প্রতিষ্ঠানের ঠিকানা", blank=True, default="")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="লোগো")
    
    # Background
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True, verbose_name="ব্যাকগ্রাউন্ড ছবি")
    background_color = models.CharField(max_length=20, default="#1e3a5f", verbose_name="ব্যাকগ্রাউন্ড কালার")
    gradient_start = models.CharField(max_length=20, default="#667eea", verbose_name="গ্রেডিয়েন্ট শুরু")
    gradient_end = models.CharField(max_length=20, default="#764ba2", verbose_name="গ্রেডিয়েন্ট শেষ")
    
    # Card colors
    card_primary_color = models.CharField(max_length=20, default="#4f46e5", verbose_name="কার্ড প্রাইমারি কালার")
    card_secondary_color = models.CharField(max_length=20, default="#7c3aed", verbose_name="কার্ড সেকেন্ডারি কালার")
    text_color = models.CharField(max_length=20, default="#ffffff", verbose_name="টেক্সট কালার")
    
    # Field visibility
    show_name = models.BooleanField(default=True, verbose_name="নাম দেখাবে")
    show_class = models.BooleanField(default=True, verbose_name="ক্লাস দেখাবে")
    show_roll = models.BooleanField(default=True, verbose_name="রোল দেখাবে")
    show_designation = models.BooleanField(default=True, verbose_name="পদবি দেখাবে")
    show_blood_group = models.BooleanField(default=True, verbose_name="ব্লাড গ্রুপ দেখাবে")
    show_address = models.BooleanField(default=True, verbose_name="ঠিকানা দেখাবে")
    show_phone = models.BooleanField(default=True, verbose_name="ফোন দেখাবে")
    show_email = models.BooleanField(default=True, verbose_name="ইমেইল দেখাবে")
    show_profile_pic = models.BooleanField(default=True, verbose_name="প্রোফাইল পিক দেখাবে")
    show_qr = models.BooleanField(default=True, verbose_name="QR কোড দেখাবে")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ইভেন্ট সেটিংস"
        verbose_name_plural = "ইভেন্ট সেটিংস"

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class DeveloperCard(models.Model):
    """ডেভেলপার কার্ড - ফিক্সড"""
    name = models.CharField(max_length=100, default="ডেভেলপার", verbose_name="নাম")
    photo = models.ImageField(upload_to='developer/', blank=True, null=True, verbose_name="ছবি")
    address = models.TextField(blank=True, default="", verbose_name="ঠিকানা")
    facebook = models.URLField(blank=True, default="", verbose_name="Facebook লিংক")
    whatsapp = models.CharField(max_length=20, blank=True, default="", verbose_name="WhatsApp নম্বর")
    is_visible = models.BooleanField(default=True, verbose_name="দেখাবে")

    class Meta:
        verbose_name = "ডেভেলপার কার্ড"
        verbose_name_plural = "ডেভেলপার কার্ড"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
