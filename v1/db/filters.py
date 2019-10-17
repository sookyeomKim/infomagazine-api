from django_filters import rest_framework as filters

from v1.db.models import LandingPageDB


class DBFilter(filters.FilterSet):
    ip_v4_address = filters.CharFilter(field_name='ip_v4_address', lookup_expr='contains')
    inflow_path = filters.CharFilter(field_name='inflow_path', lookup_expr='contains')
    registered_date_gte = filters.CharFilter(field_name='registered_date', lookup_expr='gte')
    registered_date_lte = filters.CharFilter(field_name='registered_date', lookup_expr='lte')

    class Meta:
        model = LandingPageDB
        fields = ['ip_v4_address', 'inflow_path', 'registered_date_gte', 'registered_date_lte']
