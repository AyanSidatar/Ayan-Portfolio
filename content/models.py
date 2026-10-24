from django.db import models


class Profile(models.Model):
    """Single row holding the site owner's details. Edit it in the admin."""

    name = models.CharField(max_length=120)
    headline = models.CharField(
        max_length=200,
        help_text="Short line under the name, e.g. 'Python Full Stack Developer'.",
    )
    intro = models.TextField(help_text="Hero paragraph shown under the headline.")
    about = models.TextField(
        help_text="About section. Separate paragraphs with a blank line."
    )
    mission = models.TextField(blank=True, help_text="Optional pull-quote under About.")
    location = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="profile/", blank=True)
    resume = models.FileField(upload_to="resume/", blank=True)
    available_for_work = models.BooleanField(
        default=True, help_text="Shows the 'Currently available' badge."
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profile"

    def __str__(self):
        return self.name

    @classmethod
    def load(cls):
        """Return the one profile row, or None if it hasn't been created."""
        return cls.objects.first()

    def paragraphs(self):
        return [p.strip() for p in self.about.split("\n\n") if p.strip()]


class SkillCategory(models.TextChoices):
    FRONTEND = "frontend", "Frontend"
    BACKEND = "backend", "Backend"
    DATABASE = "database", "Database"
    TOOLS = "tools", "Tools & workflow"


class Skill(models.Model):
    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=SkillCategory.choices)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Experience(models.Model):
    role = models.CharField(max_length=120)
    organization = models.CharField(max_length=120)
    period = models.CharField(max_length=60, help_text="e.g. '2023 - Present'")
    location = models.CharField(max_length=80, blank=True)
    description = models.TextField(help_text="One bullet per line.")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name_plural = "experience"

    def __str__(self):
        return f"{self.role} at {self.organization}"

    def bullets(self):
        return [line.strip() for line in self.description.splitlines() if line.strip()]


class Education(models.Model):
    degree = models.CharField(max_length=160)
    institution = models.CharField(max_length=160)
    period = models.CharField(max_length=60)
    details = models.CharField(
        max_length=200, blank=True, help_text="Optional, e.g. percentage or CGPA."
    )
    coursework = models.CharField(max_length=300, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name_plural = "education"

    def __str__(self):
        return self.degree


class Project(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField()
    tech = models.CharField(
        max_length=200, help_text="Comma-separated, e.g. 'Django, PostgreSQL, Tailwind CSS'."
    )
    image = models.ImageField(upload_to="projects/", blank=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    featured = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech.split(",") if t.strip()]
