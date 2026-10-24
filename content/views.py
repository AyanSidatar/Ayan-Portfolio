from collections import OrderedDict

from django.shortcuts import render

from contact.forms import ContactForm

from .models import Education, Experience, Profile, Project, Skill, SkillCategory


def build_context(contact_form=None):
    skill_groups = OrderedDict(
        (label, []) for _, label in SkillCategory.choices
    )
    labels = dict(SkillCategory.choices)
    for skill in Skill.objects.all():
        skill_groups[labels[skill.category]].append(skill)

    projects = list(Project.objects.filter(featured=True))
    # Filter chips for the projects grid: every technology that appears in a featured project.
    project_filters = sorted({tech for p in projects for tech in p.tech_list()}, key=str.lower)

    return {
        "profile": Profile.load(),
        "skill_groups": {k: v for k, v in skill_groups.items() if v},
        "experiences": Experience.objects.all(),
        "educations": Education.objects.all(),
        "projects": projects,
        "project_filters": project_filters,
        # Phrases cycled in the hero. Taken from the resume's own wording.
        "typing_words": [
            "Django REST APIs",
            "React interfaces",
            "PostgreSQL data models",
            "Responsive Tailwind UIs",
        ],
        "contact_form": contact_form or ContactForm(),
    }


def home(request):
    return render(request, "content/home.html", build_context())
