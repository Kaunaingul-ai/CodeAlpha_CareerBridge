
from django.contrib import admin

from .models import (
    EmployerProfile,
    CandidateProfile,
    Job,
    Resume,
    JobApplication,
)


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "company_name", "user", "location")
    search_fields = ("company_name", "user__username", "location")


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "user", "location")
    search_fields = ("full_name", "user__username", "skills")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "employer",
        "job_type",
        "is_active",
        "created_at",
    )
    list_filter = ("job_type", "is_active")
    search_fields = ("title", "description", "employer__company_name")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "candidate", "uploaded_at")
    search_fields = ("candidate__full_name",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "candidate", "status", "applied_at")
    list_filter = ("status",)
    search_fields = ("job__title", "candidate__full_name")
