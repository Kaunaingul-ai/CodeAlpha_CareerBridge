
from django.shortcuts import render
from django.db.models import Q

from jobs.models import Job


def home(request):
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()

    jobs = Job.objects.filter(is_active=True).select_related(
        "employer"
    )

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(employer__company_name__icontains=search)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    total_jobs = jobs.count()

    featured_jobs = jobs.order_by("-created_at", "-id")[:6]

    context = {
        "featured_jobs": featured_jobs,
        "total_jobs": total_jobs,
        "search": search,
        "location": location,
    }

    return render(request, "home.html", context)
