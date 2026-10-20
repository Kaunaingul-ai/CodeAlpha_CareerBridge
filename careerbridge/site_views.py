from jobs.models import CandidateProfile, EmployerProfile, Resume, JobApplication
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from jobs.models import Job

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from jobs.models import CandidateProfile, Resume, JobApplication
from jobs.serializers import JobApplicationSerializer


def home(request):
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()

    jobs = Job.objects.filter(
        is_active=True
    ).select_related("employer")

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(employer__company_name__icontains=search)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    total_jobs = jobs.count()

    featured_jobs = jobs.order_by(
        "-created_at", "-id"
    )[:6]

    return render(
        request,
        "home.html",
        {
            "featured_jobs": featured_jobs,
            "total_jobs": total_jobs,
            "search": search,
            "location": location,
        },
    )


def job_list(request):
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()
    job_type = request.GET.get("job_type", "").strip()

    jobs = Job.objects.filter(
        is_active=True
    ).select_related("employer")

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(employer__company_name__icontains=search)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        valid_job_types = [
    value for value, label in Job._meta.get_field("job_type").choices
]
        if job_type in valid_job_types:
            jobs = jobs.filter(job_type=job_type)

    jobs = jobs.order_by("-created_at", "-id")

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "search": search,
            "location": location,
            "selected_job_type": job_type,
            "job_types": Job._meta.get_field("job_type").choices,
            "total_jobs": jobs.count(),
        },
    )


def job_detail(request, job_id):
    job = get_object_or_404(
        Job.objects.select_related("employer"),
        id=job_id,
        is_active=True,
    )

    return render(
        request,
        "jobs/job_detail.html",
        {"job": job},
    )


@login_required(login_url="/api-auth/login/")
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    try:
        candidate = CandidateProfile.objects.get(user=request.user)
    except CandidateProfile.DoesNotExist:
        return HttpResponseForbidden(
            "Only candidates with a candidate profile can apply for jobs."
        )

    resumes = Resume.objects.filter(
        candidate=candidate
    ).order_by("-uploaded_at")

    existing_application = JobApplication.objects.filter(
        job=job,
        candidate=candidate
    ).exists()

    if existing_application:
        return render(
            request,
            "jobs/application_result.html",
            {
                "job": job,
                "already_applied": True,
            },
        )

    if request.method == "POST":
        data = {
            "job": job.id,
            "resume": request.POST.get("resume"),
            "cover_letter": request.POST.get(
                "cover_letter", ""
            ),
        }

        serializer = JobApplicationSerializer(
            data=data,
            context={"request": request},
        )

        if serializer.is_valid():
            try:
                from django.db import IntegrityError, transaction

                with transaction.atomic():
                    serializer.save(candidate=candidate)

            except IntegrityError:
                return render(
                    request,
                    "jobs/application_result.html",
                    {
                        "job": job,
                        "already_applied": True,
                    },
                )

            return redirect(
                "application-success-page",
                job_id=job.id,
            )

        errors = serializer.errors
    else:
        errors = None

    return render(
        request,
        "jobs/apply.html",
        {
            "job": job,
            "resumes": resumes,
            "errors": errors,
        },
    )


@login_required(login_url="/api-auth/login/")
def application_success(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
    )

    candidate = get_object_or_404(
        CandidateProfile,
        user=request.user,
    )

    application = get_object_or_404(
        JobApplication,
        job=job,
        candidate=candidate,
    )

    return render(
        request,
        "jobs/application_result.html",
        {
            "job": job,
            "application": application,
            "already_applied": False,
        },
    )


@login_required(login_url="/api-auth/login/")
def candidate_dashboard(request):
    candidate = CandidateProfile.objects.filter(
        user=request.user
    ).first()

    if candidate is None:
        return HttpResponseForbidden(
            "This dashboard is available to candidates only."
        )

    applications = (
        JobApplication.objects
        .filter(candidate=candidate)
        .select_related("job", "job__employer", "resume")
        .order_by("-applied_at")
    )

    total_applications = applications.count()

    shortlisted_count = applications.filter(
        status="shortlisted"
    ).count()

    pending_count = applications.filter(
        status="pending"
    ).count()

    resumes_count = Resume.objects.filter(
        candidate=candidate
    ).count()

    return render(
        request,
        "dashboard/candidate_dashboard.html",
        {
            "candidate": candidate,
            "applications": applications,
            "total_applications": total_applications,
            "shortlisted_count": shortlisted_count,
            "pending_count": pending_count,
            "resumes_count": resumes_count,
        },
    )


@login_required(login_url="/api-auth/login/")
def employer_dashboard(request):
    employer = EmployerProfile.objects.filter(
        user=request.user
    ).first()

    if employer is None:
        return HttpResponseForbidden(
            "This dashboard is available to employers only."
        )

    jobs = (
        Job.objects
        .filter(employer=employer)
        .order_by("-created_at")
    )

    applications = (
        JobApplication.objects
        .filter(job__employer=employer)
        .select_related(
            "job",
            "candidate",
            "resume",
        )
        .order_by("-applied_at")
    )

    context = {
        "employer": employer,
        "jobs": jobs,
        "applications": applications,
        "total_jobs": jobs.count(),
        "active_jobs": jobs.filter(is_active=True).count(),
        "total_applications": applications.count(),
        "pending_applications": applications.filter(
            status="pending"
        ).count(),
    }

    return render(
        request,
        "dashboard/employer_dashboard.html",
        context,
    )
