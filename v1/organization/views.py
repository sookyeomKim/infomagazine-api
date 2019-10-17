from rest_framework import permissions

import v1.permissions as custom_permissions
from infomagazine.custom_packages import CustomModelViewSet
from v1.organization.filters import OrganizationFilter
from v1.organization.models import Organization
from v1.organization.serializers import OrganizationSerializer


class OrganizationViewSets(CustomModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [custom_permissions.IsGuest]
        elif self.action == 'retrieve':
            permission_classes = [custom_permissions.IsMarketer]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [custom_permissions.IsOwner]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
