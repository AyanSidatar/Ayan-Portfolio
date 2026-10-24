from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Education, Experience, Profile, Project, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("name", "headline", "intro", "photo", "available_for_work")}),
        ("About", {"fields": ("about", "mission")}),
        ("Contact & links", {"fields": ("email", "phone", "location", "github_url", "linkedin_url")}),
        ("Files", {"fields": ("resume",)}),
    )

    def has_add_permission(self, request):
        # The site has exactly one profile.
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        profile = Profile.objects.first()
        if profile:
            return HttpResponseRedirect(
                reverse("admin:content_profile_change", args=[profile.pk])
            )
        return super().changelist_view(request, extra_context)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "order"]
    list_editable = ["category", "order"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["role", "organization", "period", "order"]
    list_editable = ["order"]
    search_fields = ["role", "organization"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "period", "order"]
    list_editable = ["order"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "featured", "order"]
    list_editable = ["featured", "order"]
    list_filter = ["featured"]
    search_fields = ["title", "tech"]
