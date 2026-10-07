# Django ID Card System — Vercel Deployment (No Virtual Environment)

এই project deploy করতে **virtual environment (`venv`) লাগবে না**। আপনার system Python-এ packages install করলেই হবে।

## ১. Local setup

```powershell
py --version
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

কোনো `venv` create বা activate করবেন না।

যদি `py` কাজ না করে:

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## ২. GitHub

`manage.py` যেই folder-এ আছে, সেই folder-কে repository root হিসেবে push করুন।

```powershell
git init
git add .
git commit -m "Deploy Django ID Card System to Vercel"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/idcard-system.git
git push -u origin main
```

`venv/`, `.venv/`, `env/`, `.env`, `db.sqlite3` এবং `__pycache__/` push করবেন না।

## ৩. Neon PostgreSQL

Production database হিসেবে Neon PostgreSQL ব্যবহার করুন। Vercel environment variable:

```text
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

## ৪. Cloudinary

Uploaded profile picture, logo এবং notice PDF স্থায়ীভাবে রাখার জন্য:

```text
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

## ৫. Vercel Environment Variables

```text
DJANGO_SECRET_KEY=<long-random-secret>
DEBUG=False
ALLOWED_HOSTS=.vercel.app
DATABASE_URL=<Neon connection string>
CLOUDINARY_CLOUD_NAME=<Cloudinary cloud name>
CLOUDINARY_API_KEY=<Cloudinary API key>
CLOUDINARY_API_SECRET=<Cloudinary API secret>
CSRF_TRUSTED_ORIGINS=https://YOUR-PROJECT.vercel.app
```

Custom domain ব্যবহার করলে সেটিও `ALLOWED_HOSTS` এবং `CSRF_TRUSTED_ORIGINS`-এ যোগ করুন।

## ৬. Vercel Deploy

Vercel → **Add New Project** → GitHub repository import করুন।

`manage.py` যেই folder-এ আছে সেটিই Root Directory হিসেবে নির্বাচন করুন। Current Django integration-এর জন্য `vercel.json` বা `api/index.py` wrapper দরকার নেই।

## ৭. Database migration

System Python থেকেই Neon database-এ migration চালানো যাবে:

```powershell
py manage.py migrate
py manage.py createsuperuser
```

`.env` ব্যবহার করলে সেটি GitHub-এ commit করবেন না।

## ৮. গুরুত্বপূর্ণ

Vercel runtime filesystem permanent upload storage হিসেবে ব্যবহার করবেন না। Cloudinary credentials configure করলে project Cloudinary storage ব্যবহার করবে।

ID card PDF memory-এর মধ্যে তৈরি হয়।

## ৯. Bengali PDF

Project-এর মধ্যে Noto Sans Bengali fonts আছে এবং Pillow RAQM থাকলে সেটি ব্যবহার করে; না থাকলে BASIC layout fallback ব্যবহার করে। ফলে আগের `without libraqm` crash আর হওয়ার কথা নয়।
