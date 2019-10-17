from django_filters import rest_framework as filters

from v1.company.models import Company


class CompanyFilter(filters.FilterSet):
    # users = filters.CharFilter(field_name='users', method='users_custom_filter')
    users = filters.CharFilter(field_name='users', lookup_expr='id')
    corp_name = filters.CharFilter(field_name='corp_name', lookup_expr='contains')
    corp_sub_name = filters.CharFilter(field_name='corp_sub_name', lookup_expr='contains')
    corp_header = filters.CharFilter(field_name='corp_header', lookup_expr='contains')
    corp_address = filters.CharFilter(field_name='corp_address', lookup_expr='contains')
    corp_num = filters.CharFilter(field_name='corp_num', lookup_expr='contains')
    corp_desc = filters.CharFilter(field_name='corp_desc', lookup_expr='contains')

    class Meta:
        model = Company
        fields = ['users', 'corp_name', 'corp_sub_name', 'corp_header', 'corp_address', 'corp_num', 'corp_desc']

    def users_custom_filter(self, queryset, name, value):
        lookup = {
            '__'.join([name, 'id']): value,
        }
        return queryset.filter(**lookup)
