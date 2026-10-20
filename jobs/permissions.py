
from rest_framework import permissions

from .models import EmployerProfile, CandidateProfile


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and EmployerProfile.objects.filter(
                user=request.user
            ).exists()
        )


class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.employer.user_id == request.user.id
        )



class IsCandidate(permissions.BasePermission):
    """
    Allow only authenticated users with a candidate profile.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and CandidateProfile.objects.filter(
                user=request.user
            ).exists()
        )
