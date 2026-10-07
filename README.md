# আইডি কার্ড সিস্টেম — Django + Vercel + Neon + Cloudinary

এই project-টি **Vercel-ready** এবং **virtual environment ছাড়া** ব্যবহার করার জন্য প্রস্তুত।

> **গুরুত্বপূর্ণ:** এই ZIP-এর ভিতরে `venv/`, `env/`, activation script বা local Python environment নেই। আপনার Windows system Python-এ সরাসরি packages install করবেন। GitHub-এও কোনো virtual environment push করবেন না।

Vercel-এর বর্তমান Django integration `manage.py`/WSGI structure শনাক্ত করতে পারে, তাই আলাদা `vercel.json` বা `/api` wrapper প্রয়োজন নেই।

## Stack

- Django
- PostgreSQL / Neon (production database)
- Cloudinary (profile photo, logo, notice files)
- WhiteNoise / Django staticfiles
- Pillow + bundled Noto Sans Bengali fonts
- ReportLab (ID card PDF)
- QR Code
- Jazzmin Admin

## 1. Local setup — NO virtual environment

### Windows PowerShell / CMD

প্রথমে নিশ্চিত করুন Python 3.13 installed আছে:

```powershell
py --version
```

তারপর project root-এ গিয়ে system Python-এ packages install করুন:

```powershell
cd C:\path\to\idcard_project
py -m pip install -r requirements.txt
```

**কোনো `python -m venv`, `venv\\Scripts\\activate` বা activation command প্রয়োজন নেই।**

তারপর:

```powershell
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

### If `py` command is unavailable

```powershell
python --version
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 2. GitHub — what to upload

Upload the project root containing `manage.py`.

```text
manage.py
requirements.txt
pyproject.toml
idcard_system/
cards/
core/
notices/
templates/
static/
```

Do **not** upload:

```text
venv/
.venv/
env/
__pycache__/
*.pyc
.env
db.sqlite3
media/
staticfiles/
```

The included `.gitignore` already ignores these local files/folders.

## 3. Create a Neon PostgreSQL database

Use a Neon PostgreSQL connection string as `DATABASE_URL`:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

For production, PostgreSQL is recommended instead of SQLite.

## 4. Create a Cloudinary account

Use Cloudinary for persistent uploaded profile pictures, logos and notice PDFs.

Set:

```text
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

## 5. Vercel environment variables

In Vercel → Project → Settings → Environment Variables, add:

```text
DJANGO_SECRET_KEY=<long-random-secret>
DEBUG=False
ALLOWED_HOSTS=.vercel.app
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
CLOUDINARY_CLOUD_NAME=<cloudinary-cloud-name>
CLOUDINARY_API_KEY=<cloudinary-api-key>
CLOUDINARY_API_SECRET=<cloudinary-api-secret>
CSRF_TRUSTED_ORIGINS=https://YOUR-PROJECT.vercel.app
```

For a custom domain, include it too:

```text
ALLOWED_HOSTS=.vercel.app,yourdomain.com
CSRF_TRUSTED_ORIGINS=https://YOUR-PROJECT.vercel.app,https://yourdomain.com
```

## 6. Deploy to Vercel

1. Push this project to GitHub.
2. Open Vercel.
3. Select **Add New Project**.
4. Import the GitHub repository.
5. Set **Root Directory** to the folder containing `manage.py` if needed.
6. Let Vercel auto-detect Django.
7. Add the environment variables above.
8. Deploy.

No `vercel.json` and no `api/index.py` are required by the current Django integration.

## 7. Run migrations without a virtual environment

You can run migrations from your normal system Python installation. Set the same production `DATABASE_URL` temporarily in `.env` and run:

```powershell
py manage.py migrate
py manage.py createsuperuser
```

Do not commit `.env` to GitHub.

For preview deployments, avoid blindly running migrations against the same production database. If you automate migrations, use an appropriate database branching strategy.

## 8. Vercel filesystem and uploads

Do not depend on Vercel's runtime filesystem for permanent uploads. When Cloudinary credentials are configured, this project uses Cloudinary storage for media.

The ID card PDF is generated in memory, so it does not require permanent local storage.

## 9. Bengali PDF fix

The project bundles:

```text
static/fonts/NotoSansBengali-Regular.ttf
static/fonts/NotoSansBengali-Bold.ttf
```

Pillow uses RAQM when available and falls back to BASIC layout when RAQM/libraqm is unavailable. This prevents the previous `setting text direction... without libraqm` crash.

## 10. Useful URLs

```text
/
/admin/
/register/
/card/<student-uuid>/pdf/
```

## Production checklist

- [ ] Python 3.13 installed locally
- [ ] Packages installed directly with `py -m pip install -r requirements.txt`
- [ ] No virtual environment committed
- [ ] GitHub repository contains `manage.py` at the Vercel root
- [ ] Neon `DATABASE_URL` added
- [ ] Cloudinary credentials added
- [ ] `DJANGO_SECRET_KEY` added
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` configured
- [ ] `CSRF_TRUSTED_ORIGINS` configured
- [ ] `py manage.py migrate` completed against Neon
- [ ] Superuser created
- [ ] Admin login tested
- [ ] Student registration tested
- [ ] Profile image upload tested
- [ ] ID card PDF tested
- [ ] Bengali PDF text tested
- [ ] Notice PDF upload/download tested
