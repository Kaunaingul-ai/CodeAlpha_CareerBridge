
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import (
    CandidateProfile,
    EmployerProfile,
    Job,
    Resume,
    JobApplication,
)


User = get_user_model()


# ==========================================================
# TEST 1: Candidate and Employer Permissions
# ==========================================================

class CareerBridgePermissionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.candidate_user = User.objects.create_user(
            username="test_candidate",
            password="CandidateTestPassword123!",
        )

        CandidateProfile.objects.create(
            user=self.candidate_user,
            full_name="Test Candidate",
            skills="Python, Django",
            location="Peshawar",
        )

    def test_candidate_cannot_create_employer_job(self):
        self.client.force_authenticate(
            user=self.candidate_user
        )

        response = self.client.post(
            "/api/employer/jobs/",
            {
                "title": "Unauthorized Job",
                "description": "This should be rejected.",
                "location": "Online",
                "job_type": "full_time",
                "salary": "50000.00",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)


# ==========================================================
# TESTS 2 AND 3: Employer Job Ownership
# ==========================================================

class CareerBridgeJobOwnershipTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.employer_one = User.objects.create_user(
            username="employer_one",
            password="EmployerTest123!",
        )

        self.employer_two = User.objects.create_user(
            username="employer_two",
            password="EmployerTest456!",
        )

        self.profile_one = EmployerProfile.objects.create(
            user=self.employer_one,
            company_name="Company One",
            location="Islamabad",
        )

        EmployerProfile.objects.create(
            user=self.employer_two,
            company_name="Company Two",
            location="Lahore",
        )

        self.job = Job.objects.create(
            employer=self.profile_one,
            title="Python Developer",
            description="Test job for ownership checks.",
            location="Islamabad",
            job_type="full_time",
            salary="50000.00",
            is_active=True,
        )

    def test_other_employer_cannot_edit_job(self):
        self.client.force_authenticate(
            user=self.employer_two
        )

        response = self.client.patch(
            f"/api/employer/jobs/{self.job.id}/",
            {"title": "Unauthorized Change"},
            format="json",
        )

        self.assertEqual(response.status_code, 404)

        self.job.refresh_from_db()

        self.assertEqual(
            self.job.title,
            "Python Developer",
        )

    def test_other_employer_cannot_delete_job(self):
        self.client.force_authenticate(
            user=self.employer_two
        )

        response = self.client.delete(
            f"/api/employer/jobs/{self.job.id}/"
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Job.objects.filter(
                id=self.job.id
            ).exists()
        )


# ==========================================================
# TESTS 4 AND 5: Job Applications and Status Security
# ==========================================================

class CareerBridgeApplicationTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Store test resumes in a temporary directory.
        cls._temp_media = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._temp_media.cleanup)

        cls._media_override = override_settings(
            MEDIA_ROOT=cls._temp_media.name
        )
        cls._media_override.enable()
        cls.addClassCleanup(cls._media_override.disable)

    def setUp(self):
        self.client = APIClient()

        self.employer_user = User.objects.create_user(
            username="application_employer",
            password="EmployerTest123!",
        )

        self.candidate_user = User.objects.create_user(
            username="application_candidate",
            password="CandidateTest123!",
        )

        self.employer_profile = EmployerProfile.objects.create(
            user=self.employer_user,
            company_name="CareerBridge Test Company",
            location="Islamabad",
        )

        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            full_name="Test Candidate",
            skills="Python, Django",
            location="Peshawar",
        )

        self.job = Job.objects.create(
            employer=self.employer_profile,
            title="Junior Python Developer",
            description="Test vacancy.",
            location="Islamabad",
            job_type="full_time",
            salary="50000.00",
            is_active=True,
        )

        self.resume = Resume.objects.create(
            candidate=self.candidate_profile,
            file=SimpleUploadedFile(
                "test_resume.pdf",
                b"%PDF-1.4\n%%EOF",
                content_type="application/pdf",
            ),
        )

    # ------------------------------------------------------
    # TEST 4: Duplicate Application Prevention
    # ------------------------------------------------------

    def test_candidate_cannot_apply_twice(self):
        self.client.force_authenticate(
            user=self.candidate_user
        )

        application_data = {
            "job": self.job.id,
            "resume": self.resume.id,
            "cover_letter": "Test application.",
        }

        first_response = self.client.post(
            "/api/candidate/applications/",
            application_data,
            format="json",
        )

        second_response = self.client.post(
            "/api/candidate/applications/",
            application_data,
            format="json",
        )

        self.assertEqual(
            first_response.status_code,
            201,
        )

        self.assertEqual(
            second_response.status_code,
            400,
        )

        self.assertEqual(
            JobApplication.objects.filter(
                job=self.job,
                candidate=self.candidate_profile,
            ).count(),
            1,
        )

    # ------------------------------------------------------
    # TEST 5: Prevent Unauthorized Application Status Updates
    # ------------------------------------------------------

    def test_other_employer_cannot_update_application_status(self):
        other_employer = User.objects.create_user(
            username="other_application_employer",
            password="OtherEmployerTest123!",
        )

        EmployerProfile.objects.create(
            user=other_employer,
            company_name="Other Test Company",
            location="Lahore",
        )

        application = JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_profile,
            resume=self.resume,
            status="pending",
        )

        self.client.force_authenticate(
            user=other_employer
        )

        response = self.client.patch(
            f"/api/employer/applications/{application.id}/status/",
            {"status": "shortlisted"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            404,
        )

        application.refresh_from_db()

        self.assertEqual(
            application.status,
            "pending",
        )



    def test_candidate_can_download_own_resume(self):
        self.client.force_authenticate(
            user=self.candidate_user
        )

        response = self.client.get(
            f"/api/resumes/{self.resume.id}/download/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/pdf",
        )
        self.assertTrue(response.streaming)
        response.close()

    def test_employer_can_download_applicant_resume(self):
        JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_profile,
            resume=self.resume,
            status="pending",
        )

        self.client.force_authenticate(
            user=self.employer_user
        )

        response = self.client.get(
            f"/api/resumes/{self.resume.id}/download/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)
        response.close()

    def test_unrelated_employer_cannot_download_resume(self):
        other_user = User.objects.create_user(
            username="unrelated_resume_employer",
            password="OtherEmployerTest123!",
        )

        EmployerProfile.objects.create(
            user=other_user,
            company_name="Unrelated Company",
            location="Lahore",
        )

        JobApplication.objects.create(
            job=self.job,
            candidate=self.candidate_profile,
            resume=self.resume,
            status="pending",
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.get(
            f"/api/resumes/{self.resume.id}/download/"
        )

        self.assertEqual(response.status_code, 404)
