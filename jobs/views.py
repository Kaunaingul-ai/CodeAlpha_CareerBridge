
from django.db.models import Q
from rest_framework import generics

from .serializers import ApplicationStatusSerializer
from .models import Job
from .serializers import JobSerializer

from .serializers import EmployerApplicationSerializer
from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from .models import JobApplication
from .serializers import JobApplicationSerializer

from rest_framework.parsers import MultiPartParser, FormParser

from .models import CandidateProfile
from .permissions import IsCandidate
from .serializers import ResumeSerializer

from rest_framework.permissions import IsAuthenticated


from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Resume, JobApplication

from .models import EmployerProfile
from .permissions import IsEmployer, IsJobOwner

class JobListAPIView(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.filter(
            is_active=True
        ).select_related("employer")

        keyword = self.request.query_params.get(
            "search", ""
        ).strip()

        location = self.request.query_params.get(
            "location", ""
        ).strip()

        job_type = self.request.query_params.get(
            "job_type", ""
        ).strip()

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(employer__company_name__icontains=keyword)
            )

        if location:
            queryset = queryset.filter(
                location__icontains=location
            )

        if job_type:
            queryset = queryset.filter(
                job_type=job_type
            )

        return queryset.order_by("-created_at", "-id")

class EmployerJobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def perform_create(self, serializer):
        employer = EmployerProfile.objects.get(
            user=self.request.user
        )
        serializer.save(employer=employer)


class EmployerJobManageAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
        IsJobOwner,
    ]

    def get_queryset(self):
        return Job.objects.filter(
            employer__user=self.request.user
        ).select_related("employer")


class CandidateResumeUploadAPIView(generics.CreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated, IsCandidate]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        candidate = CandidateProfile.objects.get(
            user=self.request.user
        )
        serializer.save(candidate=candidate)


class CandidateJobApplyAPIView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def perform_create(self, serializer):
        candidate = CandidateProfile.objects.get(
            user=self.request.user
        )

        try:
            with transaction.atomic():
                serializer.save(candidate=candidate)
        except IntegrityError:
            raise ValidationError(
                "You have already applied for this job."
            )


class CandidateApplicationListAPIView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):
        return JobApplication.objects.filter(
            candidate__user=self.request.user
        ).select_related(
            "job", "resume"
        ).order_by("-applied_at")


class EmployerApplicationListAPIView(generics.ListAPIView):
    serializer_class = EmployerApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return JobApplication.objects.filter(
            job__employer__user=self.request.user
        ).select_related(
            "job",
            "candidate",
            "resume",
        ).order_by("-applied_at", "-id")


class EmployerApplicationStatusAPIView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    http_method_names = ["patch", "options"]

    def get_queryset(self):
        return JobApplication.objects.filter(
            job__employer__user=self.request.user
        )


class ProtectedResumeDownloadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk)

        is_owner = (
            resume.candidate.user_id == request.user.id
        )

        is_authorized_employer = (
            JobApplication.objects.filter(
                resume=resume,
                job__employer__user=request.user
            ).exists()
        )

        if not (is_owner or is_authorized_employer):
            raise Http404("Resume not found.")

        if not resume.file:
            raise Http404("Resume file not found.")

        try:
            file_handle = resume.file.open("rb")
        except (FileNotFoundError, OSError):
            raise Http404("Resume file not found.")

        response = FileResponse(
            file_handle,
            content_type="application/pdf",
            as_attachment=True,
            filename="candidate_resume.pdf",
        )
        response["Cache-Control"] = "private, no-store"
        response["X-Content-Type-Options"] = "nosniff"

        return response
