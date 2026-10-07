from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import StudentRegistrationForm
from .models import Student
from core.models import EventSettings
import io
import base64
from django.conf import settings as django_settings

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageDraw, ImageFont, features
from urllib.parse import quote


def _font_path(bold=False):
    base = django_settings.BASE_DIR / "static" / "fonts"
    if bold:
        p = base / "NotoSansBengali-Bold.ttf"
        if p.exists():
            return str(p)
    p = base / "NotoSansBengali-Regular.ttf"
    return str(p) if p.exists() else None


def _get_font(size, bold=False):
    """Load Bengali font without requiring libraqm.

    If RAQM is available, use it for better complex-script shaping.
    Otherwise fall back to Pillow's BASIC layout engine so Vercel/serverless
    environments without libraqm do not crash.
    """
    path = _font_path(bold)
    if path:
        try:
            if features.check("raqm"):
                return ImageFont.truetype(
                    path, size, layout_engine=ImageFont.Layout.RAQM
                )
        except Exception:
            pass
        try:
            return ImageFont.truetype(
                path, size, layout_engine=ImageFont.Layout.BASIC
            )
        except Exception:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _hex_to_rgb(hex_color, default=(79, 70, 229)):
    try:
        h = (hex_color or "").lstrip("#")
        if len(h) == 6:
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except Exception:
        pass
    return default


def _make_qr_image(data, size=130):
    if not HAS_QRCODE:
        return None
    try:
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color="black", back_color="white").convert("RGB").resize((size, size), PILImage.LANCZOS)
    except Exception:
        return None


def _rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    try:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)
    except Exception:
        draw.rectangle(xy, fill=fill, outline=outline, width=width)


def _render_id_card_image(student, settings, scale=4):
    """Premium vertical ID card — PIL (Bengali safe)"""
    W, H = 340 * scale, 540 * scale
    s = scale
    c1 = _hex_to_rgb(getattr(settings, "gradient_start", None) or "#4f46e5")
    c2 = _hex_to_rgb(getattr(settings, "gradient_end", None) or "#db2777")

    img = PILImage.new("RGB", (W, H), c1)
    draw = ImageDraw.Draw(img)

    # Smooth gradient
    for y in range(H):
        t = y / max(H - 1, 1)
        r = int(c1[0] * (1 - t) + c2[0] * t)
        g = int(c1[1] * (1 - t) + c2[1] * t)
        b = int(c1[2] * (1 - t) + c2[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Decorative circle top-right
    overlay = PILImage.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([W - 140*s, -40*s, W + 40*s, 140*s], fill=(255, 255, 255, 25))
    od.ellipse([-60*s, H - 100*s, 80*s, H + 40*s], fill=(255, 255, 255, 18))
    img = PILImage.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Header
    header_h = int(78 * s)
    draw.rectangle([0, 0, W, header_h], fill=(20, 15, 55))
    # gold accent line
    draw.rectangle([int(W*0.15), header_h - 3*s, int(W*0.85), header_h], fill=(255, 215, 100))

    font_title = _get_font(int(16 * s), bold=True)
    font_addr = _get_font(int(9 * s))
    font_label = _get_font(int(8 * s))
    font_value = _get_font(int(13 * s), bold=True)
    font_id = _get_font(int(10 * s), bold=True)

    def center_text(text, y, font, fill=(255, 255, 255)):
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=font, fill=fill)

    event_name = (settings.event_name or "ID Card")[:36]
    center_text(event_name, int(20 * s), font_title, (255, 255, 255))
    addr = (settings.institution_address or "")[:48]
    if addr:
        center_text(addr, int(44 * s), font_addr, (200, 200, 230))

    # Photo circle
    photo_size = int(115 * s)
    photo_x = (W - photo_size) // 2
    photo_y = header_h + int(18 * s)

    # Outer ring (white)
    ring = 5 * s
    draw.ellipse(
        [photo_x - ring, photo_y - ring, photo_x + photo_size + ring, photo_y + photo_size + ring],
        fill=(255, 255, 255)
    )
    # Inner gold ring
    draw.ellipse(
        [photo_x - 2*s, photo_y - 2*s, photo_x + photo_size + 2*s, photo_y + photo_size + 2*s],
        fill=(255, 200, 80)
    )

    if student.profile_picture and settings.show_profile_pic:
        try:
            with student.profile_picture.open("rb") as uploaded_photo:
                pic = PILImage.open(uploaded_photo).convert("RGB")
            pic = pic.resize((photo_size, photo_size), PILImage.LANCZOS)
            mask = PILImage.new("L", (photo_size, photo_size), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, photo_size, photo_size], fill=255)
            out = PILImage.new("RGB", (photo_size, photo_size), c1)
            out.paste(pic, mask=mask)
            img.paste(out, (photo_x, photo_y))
            draw = ImageDraw.Draw(img)
        except Exception:
            draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], fill=(180, 180, 200))
    else:
        draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], fill=(180, 180, 200))

    # Info fields
    y = photo_y + photo_size + int(16 * s)
    row_h = int(36 * s)
    pad_x = int(22 * s)

    fields = []
    if settings.show_name:
        fields.append(("নাম / Name", student.name))
    if settings.show_class and student.class_name:
        fields.append(("ক্লাস / Class", student.class_name))
    if settings.show_roll and student.roll:
        fields.append(("রোল / Roll", student.roll))
    if settings.show_designation and student.designation:
        fields.append(("পদবি / Designation", student.designation))
    if settings.show_blood_group and student.blood_group:
        fields.append(("ব্লাড গ্রুপ / Blood", student.blood_group))
    if settings.show_phone and student.phone:
        fields.append(("ফোন / Phone", student.phone))
    if settings.show_email and student.email:
        fields.append(("ইমেইল / Email", student.email))
    if settings.show_address and student.address:
        fields.append(("ঠিকানা / Address", student.address[:38]))

    for label, value in fields:
        if not value:
            continue
        # glass-like row
        _rounded_rect(
            draw,
            [pad_x, y, W - pad_x, y + row_h - 4*s],
            radius=int(8 * s),
            fill=(255, 255, 255, ) if False else (40, 30, 90),
        )
        # semi-transparent feel via darker fill
        _rounded_rect(
            draw,
            [pad_x, y, W - pad_x, y + row_h - 4*s],
            radius=int(8 * s),
            fill=(255, 255, 255),
            outline=None,
        )
        # Actually use a translucent-looking solid
        # redraw with purple-tinted white
        _rounded_rect(
            draw,
            [pad_x, y, W - pad_x, y + row_h - 4*s],
            radius=int(8 * s),
            fill=(245, 243, 255),
        )
        # label
        bbox = draw.textbbox((0, 0), str(label), font=font_label)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y + 2*s), str(label), font=font_label, fill=(100, 90, 140))
        # value
        val = str(value)[:32]
        bbox = draw.textbbox((0, 0), val, font=font_value)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y + int(13 * s)), val, font=font_value, fill=(40, 30, 90))
        y += row_h

    # QR
    if settings.show_qr:
        qr_img = _make_qr_image(student.get_qr_data(), size=int(80 * s))
        if qr_img:
            qr_x = (W - qr_img.width) // 2
            qr_y = min(y + int(6 * s), H - int(110 * s))
            pad = int(6 * s)
            _rounded_rect(
                draw,
                [qr_x - pad, qr_y - pad, qr_x + qr_img.width + pad, qr_y + qr_img.height + pad],
                radius=int(10 * s),
                fill=(255, 255, 255),
            )
            img.paste(qr_img, (qr_x, qr_y))
            draw = ImageDraw.Draw(img)

    # Footer
    fh = int(32 * s)
    draw.rectangle([0, H - fh, W, H], fill=(15, 10, 45))
    draw.rectangle([0, H - fh, W, H - fh + 2*s], fill=(255, 200, 80))
    id_text = f"ID: {student.unique_id.hex[:8].upper()}"
    center_text(id_text, H - int(22 * s), font_id, (255, 230, 150))

    return img


def home(request):
    settings = EventSettings.get_solo()
    recent = Student.objects.filter(is_active=True)[:6]
    return render(request, "cards/home.html", {
        "settings": settings,
        "recent_students": recent,
    })


def register(request):
    settings = EventSettings.get_solo()
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"রেজিস্ট্রেশন সফল! আপনার আইডি: {student.unique_id.hex[:8].upper()}")
            return redirect("card_view", uid=student.unique_id)
        messages.error(request, "ফর্ম পূরণে সমস্যা আছে। আবার চেষ্টা করুন।")
    else:
        form = StudentRegistrationForm()
    return render(request, "cards/register.html", {"form": form, "settings": settings})


def card_view(request, uid):
    student = get_object_or_404(Student, unique_id=uid, is_active=True)
    settings = EventSettings.get_solo()
    qr_base64 = None
    if settings.show_qr and HAS_QRCODE:
        try:
            qr = qrcode.QRCode(version=1, box_size=6, border=2)
            qr.add_data(student.get_qr_data())
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            qr_base64 = base64.b64encode(buf.getvalue()).decode()
        except Exception:
            pass
    return render(request, "cards/card.html", {
        "student": student,
        "settings": settings,
        "qr_base64": qr_base64,
        "has_qrcode": HAS_QRCODE,
    })


def card_pdf(request, uid):
    student = get_object_or_404(Student, unique_id=uid, is_active=True)
    settings = EventSettings.get_solo()
    card_img = _render_id_card_image(student, settings, scale=3)

    png_buf = io.BytesIO()
    card_img.save(png_buf, format="PNG")
    png_buf.seek(0)

    img_w, img_h = card_img.size
    pdf_w = 72 * mm
    pdf_h = pdf_w * (img_h / img_w)

    pdf_buf = io.BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=(pdf_w, pdf_h))
    c.drawImage(ImageReader(png_buf), 0, 0, width=pdf_w, height=pdf_h)
    c.showPage()
    c.save()
    pdf_buf.seek(0)

    # ASCII fallback + RFC 5987 UTF-8 filename for Bengali names.
    safe_name = "".join(ch for ch in student.name if ch.isalnum() or ch in " _-")[:40] or "card"
    encoded_name = quote(f"idcard_{safe_name}.pdf")
    response = HttpResponse(pdf_buf.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="idcard.pdf"; filename*=UTF-8\'\'{encoded_name}'
    )
    return response


def student_list(request):
    settings = EventSettings.get_solo()
    students = Student.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    if q:
        from django.db.models import Q
        students = students.filter(
            Q(name__icontains=q) | Q(roll__icontains=q) | Q(phone__icontains=q)
        )
    return render(request, "cards/list.html", {"students": students, "settings": settings, "q": q})
