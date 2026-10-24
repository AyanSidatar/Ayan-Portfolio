# Ayan Sidatar, Portfolio

A personal portfolio built with Django. Content is managed in the Django admin, and the
contact form saves messages to the database.

- **Backend:** Django 5.2, SQLite locally
- **Frontend:** Django templates, Tailwind CSS, a dark theme with animated "liquid" headings
- **Admin:** all profile, skill, experience, education and project content, plus contact messages

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_portfolio    # loads your content (safe to re-run)
python manage.py createsuperuser   # login for /admin/
python manage.py runserver
```

Then open http://127.0.0.1:8000 and http://127.0.0.1:8000/admin/.

Run the tests with:

```bash
python manage.py test
```

## Editing content

Everything shown on the site is editable in `/admin/`:

| Admin section | What it controls |
| --- | --- |
| Profile | Name, headline, intro, About text, photo, resume PDF, contact details, links, "available" badge |
| Skills | Grouped skill chips (frontend, backend, database, tools) |
| Experience | Roles, with one bullet per line in the description |
| Education | Degrees and coursework |
| Projects | Featured project cards, with image, summary, tech list and links |
| Messages | Contact form submissions (marked read/unread) |

To reset the seeded content to the defaults in `content/management/commands/seed_portfolio.py`,
run `python manage.py seed_portfolio --reset`. This deletes skills, experience, education and projects
first, so anything you added in the admin is lost. The profile row is updated in place.

## Contact form

Messages are always saved. To also get an email, set these environment variables:

```bash
export CONTACT_NOTIFY_EMAIL=you@example.com
export DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export EMAIL_HOST=smtp.example.com   # plus EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS
```

Without these, the notification email is printed to the console and the message is still saved.

## Deploying

The recommended free option is PythonAnywhere, which runs Django with SQLite and gives you a
free `yourname.pythonanywhere.com` address. Free-tier limits change, so check them before you deploy. Steps:

1. Set these environment variables on the host:
   - `DJANGO_SECRET_KEY`: a long random string
   - `DJANGO_DEBUG=0`
   - `DJANGO_ALLOWED_HOSTS=yourdomain.pythonanywhere.com` (comma-separated if several)
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.pythonanywhere.com`
2. Install dependencies, then run:
   ```bash
   python manage.py migrate
   python manage.py seed_portfolio
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```
3. Serve the app through the host's WSGI setup, with `config.wsgi.application` as the entry point.

**Uploaded files.** Images and the resume PDF live in `media/`, which is not committed to git.
Upload that folder to the host separately, or re-upload the files through the admin. Django does
not serve `media/` when `DEBUG` is off. On PythonAnywhere, add a static-files mapping from
`/media/` to the `media/` folder in the Web tab. Other hosts need their own mapping or cloud storage.
