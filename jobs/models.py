
from django.conf import settings
from django.db import models


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employer_profile",
    )
    company_name = models.CharField(max_length=150)
    company_website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.company_name


class CandidateProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    full_name = models.CharField(max_length=150)
    skills = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name



class Job(models.Model):
    JOB_TYPES = [
        ("full_time", "Full-Time"),
        ("part_time", "Part-Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

    employer = models.ForeignKey(
        EmployerProfile,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=150)
    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default="full_time",
    )
    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resume(models.Model):
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="resumes",
    )
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume - {self.candidate.full_name}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    resume = models.ForeignKey(
        Resume,
        on_delete=models.PROTECT,
        related_name="applications",
    )
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job", "candidate"],
                name="unique_candidate_job_application",
            )
        ]

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title}"
