from rest_framework import permissions

import v1.permissions as custom_permissions
from v1.company.filters import CompanyFilter
from v1.company.models import Company
from v1.company.serializers import CompanySerializer
from infomagazine.custom_packages import CustomModelViewSet
from v1.user.models import AccessRole


class CompanyViewSets(CustomModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter

    def get_queryset(self):
        if self.action == 'list':
            if not self.request.user.is_staff:
                filter_fields = {
                    'users__info__organization_id': self.request.user.info.organization_id,
                }
                if self.request.user.info.access_role == AccessRole.CLIENT:
                    filter_fields.update({'users__id': self.request.user_id})
                return self.queryset.filter(**filter_fields).distinct()
        return self.queryset.all()

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [custom_permissions.IsClient]
        else:
            permission_classes = [custom_permissions.IsMarketer]
        return [permission() for permission in permission_classes]
