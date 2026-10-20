
from django.contrib import admin
from django.urls import include, path


from .site_views import (
    home,
    job_list,
    job_detail,
    apply_for_job,
    application_success,
    candidate_dashboard,
    employer_dashboard,
)

from .site_views import (
    home,
    job_list,
    job_detail,
    apply_for_job,
    application_success,
)

urlpatterns = [
    # Main website
    path("", home, name="home"),

    # Job browsing
    path("jobs/", job_list, name="job-list-page"),
    path(
        "jobs/<int:job_id>/",
        job_detail,
        name="job-detail-page",
    ),
    path(
    "jobs/<int:job_id>/application-success/",
    application_success,
    name="application-success-page",
),

    # Candidate application form
    path(
        "jobs/<int:job_id>/apply/",
        apply_for_job,
        name="job-apply-page",
    ),

    # Django administration
    path("admin/", admin.site.urls),

    # Django REST Framework authentication
    path("api-auth/", include("rest_framework.urls")),

    # Existing backend APIs
    path("api/", include("jobs.urls")),

    path(
    "dashboard/candidate/",
    candidate_dashboard,
    name="candidate-dashboard",
),
    path(
    "dashboard/employer/",
    employer_dashboard,
    name="employer-dashboard",
),

]
