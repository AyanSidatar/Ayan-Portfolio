"""
Load the portfolio content into the database.

Safe to run more than once: the profile is updated in place and projects,
skills, experience and education are matched by their key fields, so edits
you make in the admin are not duplicated. Use --reset to wipe and reload.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from content.models import Education, Experience, Profile, Project, Skill

GITHUB_USER = "https://github.com/AyanSidatar"
MERN_REPO = f"{GITHUB_USER}/MERN-Stack-Projects"

IMG_DIR = Path(settings.BASE_DIR) / "static" / "img"
FILE_DIR = Path(settings.BASE_DIR) / "static" / "files"

PROFILE = {
    "name": "Ayan Sidatar",
    "headline": "Python Full Stack Developer",
    "intro": (
        "Python full stack developer building web applications with Django, Flask, "
        "React.js and PostgreSQL. I care about clean code, fast pages, and interfaces "
        "people enjoy using."
    ),
    "about": "\n\n".join([
        "I'm a Python full stack developer with hands-on experience building web "
        "applications with Python, Django, Flask, and React.js.",
        "I build REST APIs with Django REST Framework, model data on PostgreSQL, and "
        "create responsive interfaces with Tailwind CSS. My earlier projects were on "
        "the MERN stack (MongoDB, Express, React and Node.js), so I'm comfortable "
        "across both ecosystems.",
        "My journey started with a curiosity for how things work on the web, and it has "
        "grown into a practical focus on modern frontend and backend development.",
        "When I'm not coding, you'll find me exploring new technologies, contributing to "
        "open-source projects, or sharing knowledge with the developer community.",
    ]),
    "mission": (
        "My mission is to create digital experiences that are not just functional, but "
        "truly delightful: products that users love to use and developers love to maintain."
    ),
    "location": "Botad, Gujarat, India (open to remote)",
    "email": "ayansidatar07@gmail.com",
    "phone": "+91 7046566750",
    "github_url": "https://github.com/AyanSidatar",
    # Your resume and old site point to different LinkedIn URLs; confirm and edit in admin.
    "linkedin_url": "https://www.linkedin.com/in/ayan-sidatar-640449369/",
    "available_for_work": True,
}

SKILLS = {
    "frontend": [
        "HTML5", "CSS3", "JavaScript (ES6+)", "React.js", "Next.js",
        "Tailwind CSS", "Responsive Web Design",
    ],
    "backend": [
        "Python", "Django", "Flask", "Django REST Framework", "RESTful APIs",
        "Node.js", "Express.js",
    ],
    "database": ["PostgreSQL", "Django ORM", "SQLAlchemy", "MongoDB"],
    "tools": [
        "Git", "GitHub", "Render", "Heroku", "pip", "virtualenv",
        "Agile", "Performance optimisation", "Lighthouse auditing",
    ],
}

EXPERIENCE = [
    {
        "role": "Python Full Stack Developer (Freelance)",
        "organization": "Self-directed projects",
        "period": "2023 - Present",
        "location": "Remote",
        "description": "\n".join([
            "Built and maintained a React.js single-page app with a Django REST Framework "
            "backend, PostgreSQL via the Django ORM, and reusable React components.",
            "Reduced page load time by refactoring Django views and React components and "
            "removing redundant API calls, measured with Google Lighthouse.",
            "Delivered end-to-end projects covering requirements, UI, API integration, "
            "testing, and deployment.",
            "Built responsive layouts with Tailwind CSS, tested across mobile, tablet and "
            "desktop screen sizes.",
        ]),
        "order": 1,
    },
    {
        # Dates and bullet points are not confirmed yet. Fill them in via the admin.
        "role": "Trainee, Python Full Stack Development",
        "organization": "TOPS Technologies Pvt. Ltd.",
        "period": "",
        "location": "",
        "description": "\n".join([
            "Completed training assignments in Python fundamentals, covering control flow, "
            "functions, collections and a mini project.",
            "Practised C and C++ programming, including object-oriented concepts such as "
            "classes and inheritance, and built a bank-account mini project.",
            "Wrote SQL queries and procedures for database operations, including a mini project.",
            "Built responsive HTML, CSS and Bootstrap layouts for mobile, tablet and desktop, "
            "recreating interfaces inspired by popular e-commerce, food-delivery and "
            "entertainment apps.",
        ]),
        "order": 2,
    },
]

EDUCATION = [
    {
        "degree": "Bachelor of Computer Application (BCA)",
        "institution": "Bhavnagar University, Gujarat, India",
        "period": "2022 - 2025",
        "details": "",
        "coursework": "Data Structures, Web Technologies, DBMS, OOP, Computer Networks",
        "order": 1,
    },
]

PROJECTS = [
    {
        "title": "Twitter / X Clone",
        "summary": (
            "A responsive social app with a user feed, post interactions and profile pages, "
            "built on a Django backend with a PostgreSQL database."
        ),
        "tech": "Python, Django, PostgreSQL, Tailwind CSS",
        "image": "Xcloan.png",
        "live_url": "",
        "github_url": MERN_REPO,
        "order": 1,
    },
    {
        "title": "Full-Stack Portfolio Website",
        "summary": (
            "A React single-page frontend backed by a Django REST API, showing my projects "
            "and the integration between the two."
        ),
        "tech": "React.js, Django REST Framework, Tailwind CSS",
        "image": "",
        "live_url": "https://ayan-pottfolio.vercel.app",
        "github_url": "https://github.com/AyanSidatar/AyanPottfolio",
        "order": 2,
    },
    {
        "title": "Interior Design Web Application",
        "summary": (
            "A multi-section site with server-side routing and template rendering, built as "
            "my final-year project."
        ),
        "tech": "Python, Flask, HTML5, CSS3",
        "image": "intirior.png",
        "live_url": "",
        "github_url": MERN_REPO,
        "order": 3,
    },
    {
        "title": "Music Streaming Web Application",
        "summary": "Playlist navigation and custom HTML5 audio controls on a Flask backend.",
        "tech": "Python, Flask, HTML5, CSS3",
        "image": "",
        "live_url": "",
        "github_url": "",
        "order": 4,
    },
    {
        "title": "Itask | Manage Your Tasks",
        "summary": (
            "A todo app that stores tasks locally and in a database, so no task gets "
            "forgotten."
        ),
        "tech": "React.js, Tailwind CSS, Node.js, MongoDB",
        "image": "todoproject.png",
        "live_url": "",
        "github_url": MERN_REPO,
        "order": 5,
    },
    {
        "title": "PassOP | Password Manager",
        "summary": (
            "Stores passwords, usernames and sites, so you don't lose access to an account "
            "you've forgotten the details of."
        ),
        "tech": "React.js, Tailwind CSS, Node.js",
        "image": "Passmanager.png",
        "live_url": "",
        "github_url": MERN_REPO,
        "order": 6,
    },
]


class Command(BaseCommand):
    help = "Load the portfolio content (profile, skills, experience, education, projects)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing skills, experience, education and projects before loading.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            Skill.objects.all().delete()
            Experience.objects.all().delete()
            Education.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write("Cleared existing portfolio items.")

        self.load_profile()
        self.load_skills()
        self.load_experience()
        self.load_education()
        self.load_projects()
        self.stdout.write(self.style.SUCCESS("Portfolio content loaded."))

    def load_profile(self):
        profile = Profile.load()
        if profile is None:
            profile = Profile(**PROFILE)
        else:
            for key, value in PROFILE.items():
                setattr(profile, key, value)

        if not profile.photo:
            self._attach(profile, "photo", IMG_DIR / "AyanProfile1.png", "profile")
        if not profile.resume:
            self._attach(profile, "resume", FILE_DIR / "AyanResume.pdf", "resume")
        profile.save()
        self.stdout.write("Profile loaded.")

    def load_skills(self):
        for category, names in SKILLS.items():
            for order, name in enumerate(names, start=1):
                Skill.objects.update_or_create(
                    name=name, category=category, defaults={"order": order}
                )
        self.stdout.write(f"Skills loaded: {Skill.objects.count()}.")

    def load_experience(self):
        for item in EXPERIENCE:
            Experience.objects.update_or_create(
                role=item["role"], organization=item["organization"], defaults=item
            )

    def load_education(self):
        for item in EDUCATION:
            Education.objects.update_or_create(
                degree=item["degree"], institution=item["institution"], defaults=item
            )

    def load_projects(self):
        for item in PROJECTS:
            data = {k: v for k, v in item.items() if k != "image"}
            project, _ = Project.objects.update_or_create(title=item["title"], defaults=data)
            if item["image"] and not project.image:
                self._attach(project, "image", IMG_DIR / item["image"], "projects")
                project.save()
        self.stdout.write(f"Projects loaded: {Project.objects.count()}.")

    def _attach(self, obj, field_name, path, subdir):
        if not path.exists():
            self.stderr.write(f"Missing file, skipped: {path}")
            return
        with path.open("rb") as handle:
            getattr(obj, field_name).save(path.name, File(handle), save=False)
