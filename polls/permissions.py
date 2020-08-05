from rest_framework.permissions import BasePermission


class PollsAdmin(BasePermission):
    """
    Checks if user have Poll perms
    """

    def has_permission(self, request, view):
        perms = [
            'polls.view_poll',
            'polls.add_poll',
            'polls.change_poll',
            'polls.delete_poll'
        ]
        for i in perms:
            if request.user.has_perm(i):
                return True
        return False
