from django.test import TestCase
from django.urls import reverse

from .models import Profile, Project, Skill


class HomePageTests(TestCase):
    def test_home_renders_without_profile(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No profile yet")

    def test_home_renders_profile_and_sections(self):
        Profile.objects.create(
            name="Test Person",
            headline="Python Full Stack Developer",
            intro="Intro text here.",
            about="First paragraph.\n\nSecond paragraph.",
            location="Somewhere",
            email="test@example.com",
        )
        Skill.objects.create(name="Django", category="backend")
        Project.objects.create(title="Demo App", summary="A demo.", tech="Django, PostgreSQL")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Person")
        self.assertContains(response, "First paragraph.")
        self.assertContains(response, "Second paragraph.")
        self.assertContains(response, "Django")
        self.assertContains(response, "Demo App")
        self.assertContains(response, 'id="contact"')

    def test_project_tech_list_is_split(self):
        project = Project(title="x", summary="y", tech="Django, PostgreSQL , Tailwind CSS")
        self.assertEqual(project.tech_list(), ["Django", "PostgreSQL", "Tailwind CSS"])

    def test_profile_paragraphs_split_on_blank_lines(self):
        profile = Profile(about="One.\n\nTwo.\n\n\nThree.")
        self.assertEqual(profile.paragraphs(), ["One.", "Two.", "Three."])
