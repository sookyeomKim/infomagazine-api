from rest_framework import serializers

from v1.organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'org_name', 'org_sub_name', 'org_crn', 'org_header', 'org_address', 'org_tel_num', 'org_desc',
                  'created_date', 'updated_date')
        extra_kwargs = {
            'created_date': {
                'read_only': True
            },
            'updated_date': {
                'read_only': True
            }
        }
