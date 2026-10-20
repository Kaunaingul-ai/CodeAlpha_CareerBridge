
from django.urls import path
from .views import CandidateJobApplyAPIView

from .views import EmployerApplicationStatusAPIView
from .views import EmployerApplicationListAPIView
from .views import CandidateApplicationListAPIView

from .views import ProtectedResumeDownloadAPIView

from .views import CandidateResumeUploadAPIView
from .views import (
    JobListAPIView,
    EmployerJobCreateAPIView,
    EmployerJobManageAPIView,
)

urlpatterns = [
    path(
        "jobs/",
        JobListAPIView.as_view(),
        name="job-list",
    ),
    path(
        "employer/jobs/",
        EmployerJobCreateAPIView.as_view(),
        name="employer-job-create",
    ),
    path(
        "employer/jobs/<int:pk>/",
        EmployerJobManageAPIView.as_view(),
        name="employer-job-manage",
    ),

    path(
        "candidate/resumes/",
        CandidateResumeUploadAPIView.as_view(),
        name="candidate-resume-upload",
    ),


    path(
        "candidate/applications/",
        CandidateJobApplyAPIView.as_view(),
        name="candidate-job-apply",
    ),


    path(
        "candidate/my-applications/",
        CandidateApplicationListAPIView.as_view(),
        name="candidate-my-applications",
    ),


    path(
        "employer/applications/",
        EmployerApplicationListAPIView.as_view(),
        name="employer-applications",
    ),


    path(
        "employer/applications/<int:pk>/status/",
        EmployerApplicationStatusAPIView.as_view(),
        name="employer-application-status",
    ),


    path(
        "resumes/<int:pk>/download/",
        ProtectedResumeDownloadAPIView.as_view(),
        name="protected-resume-download",
    ),

]
