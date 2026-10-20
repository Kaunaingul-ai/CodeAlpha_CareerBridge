
from rest_framework import serializers

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

from .models import Job, Resume, JobApplication


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="employer.company_name",
        read_only=True,
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "employer",
            "company_name",
            "title",
            "description",
            "location",
            "job_type",
            "salary",
            "is_active",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "employer",
            "company_name",
            "created_at",
        ]



class ResumeSerializer(serializers.ModelSerializer):

    file = serializers.FileField(write_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "file",
            "uploaded_at",
        ]
        read_only_fields = [
            "id",
            "uploaded_at",
        ]

    def validate_file(self, value):
        if not isinstance(value, UploadedFile):
            raise serializers.ValidationError(
                "Please upload a valid file."
            )

        if value.size > settings.MAX_RESUME_SIZE:
            raise serializers.ValidationError(
                "Resume must not exceed 2 MB."
            )

        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError(
                "Only PDF resumes are allowed."
            )

        # Check the PDF file signature.
        beginning = value.read(5)
        value.seek(0)

        if beginning != b"%PDF-":
            raise serializers.ValidationError(
                "The uploaded file is not a valid PDF."
            )

        return value


class JobApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "job_title",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]
        read_only_fields = [
            "id",
            "job_title",
            "status",
            "applied_at",
        ]

    def validate(self, attrs):
        request = self.context["request"]
        candidate = request.user.candidate_profile

        job = attrs["job"]
        resume = attrs["resume"]

        if not job.is_active:
            raise serializers.ValidationError(
                {"job": "This job is no longer accepting applications."}
            )

        if resume.candidate_id != candidate.id:
            raise serializers.ValidationError(
                {"resume": "You can only use your own resume."}
            )

        if JobApplication.objects.filter(
            job=job,
            candidate=candidate,
        ).exists():
            raise serializers.ValidationError(
                "You have already applied for this job."
            )

        return attrs


class EmployerApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job.title",
        read_only=True,
    )

    candidate_name = serializers.CharField(
        source="candidate.full_name",
        read_only=True,
    )

    class Meta:
        model = JobApplication
        fields = [
            "id",
            "job",
            "job_title",
            "candidate_name",
            "resume",
            "cover_letter",
            "status",
            "applied_at",
        ]
        read_only_fields = fields


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "status"]
        read_only_fields = ["id"]

    def validate_status(self, value):
        valid_statuses = [
            choice[0]
            for choice in JobApplication.STATUS_CHOICES
        ]

        if value not in valid_statuses:
            raise serializers.ValidationError(
                "Invalid application status."
            )

        return value
