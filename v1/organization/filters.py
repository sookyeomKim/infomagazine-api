from django_filters import rest_framework as filters

from v1.organization.models import Organization


class OrganizationFilter(filters.FilterSet):
    org_name = filters.CharFilter(field_name='org_name', lookup_expr='contains')
    org_sub_name = filters.CharFilter(field_name='org_sub_name', lookup_expr='contains')
    org_crn = filters.CharFilter(field_name='org_crn', lookup_expr='contains')
    org_header = filters.CharFilter(field_name='org_header', lookup_expr='contains')
    org_address = filters.CharFilter(field_name='org_address', lookup_expr='contains')
    org_tel_num = filters.CharFilter(field_name='org_tel_num', lookup_expr='contains')
    org_desc = filters.CharFilter(field_name='org_desc', lookup_expr='contains')

    class Meta:
        model = Organization
        fields = ['org_name', 'org_sub_name', 'org_crn', 'org_header', 'org_address', 'org_tel_num', 'org_desc']
