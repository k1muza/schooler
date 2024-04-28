from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user

from user_management.models import Guardian
from user_management.permissions.guardian import HasGuardianPermission
from user_management.serializers.guardian import GuardianSerializer

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [HasGuardianPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        perms = [
            'view_guardian',
            'change_guardian',
            'delete_guardian',
        ]
        queryset = get_objects_for_user(
            self.request.user, perms, klass=self.queryset, accept_global_perms=False, any_perm=True)
        return queryset
    