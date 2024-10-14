from rest_framework import permissions
from allauth.account.models import EmailAddress


class IsActiveAndVerified(permissions.BasePermission):
    """
    Custom permission to only allow active, authenticated users with verified emails
    and completed data to access the API.
    """

    def has_permission(self, request, view):
        user = request.user

        # Check if the user is authenticated and active
        if not user.is_authenticated or not user.is_active:
            return False

        # Check if the email is verified
        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            return False

        return True
