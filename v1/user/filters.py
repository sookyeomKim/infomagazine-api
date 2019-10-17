from django_filters import rest_framework as filters

from v1.user.models import User


class _NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class UserFilter(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='contains')
    username = filters.CharFilter(field_name='username', lookup_expr='contains')
    company = filters.NumberFilter(field_name='company', lookup_expr='id')
    organization = filters.NumberFilter(field_name='info', lookup_expr='organization_id')
    access_role = _NumberInFilter(field_name='info', lookup_expr='access_role__in')

    class Meta:
        model = User
        fields = ['email', 'username', 'company', 'organization', 'access_role']
