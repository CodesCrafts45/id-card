from django.db import models


class Notice(models.Model):
    """নোটিশ - ছবিসহ + PDF ডাউনলোড"""
    title = models.CharField(max_length=250, verbose_name="শিরোনাম")
    content = models.TextField(verbose_name="বিস্তারিত", blank=True)
    image = models.ImageField(upload_to="notices/", blank=True, null=True, verbose_name="ছবি")
    pdf_file = models.FileField(upload_to="notice_pdfs/", blank=True, null=True, verbose_name="PDF ফাইল")
    is_published = models.BooleanField(default=True, verbose_name="প্রকাশিত")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "নোটিশ"
        verbose_name_plural = "নোটিশসমূহ"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

