from rest_framework import serializers

from v1.company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id', 'corp_name', 'corp_sub_name', 'corp_header', 'corp_address', 'corp_num', 'corp_desc', 'created_date',
            'updated_date')
        extra_kwargs = {
            'created_date': {
                'read_only': True
            },
            'updated_date': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        company = Company(
            corp_name=validated_data['corp_name'],
            corp_sub_name=validated_data['corp_sub_name'],
            corp_header=validated_data['corp_header'],
            corp_address=validated_data['corp_address'],
            corp_num=validated_data['corp_num'],
            corp_desc=validated_data['corp_desc'],
        )
        company.save()
        company.users.add(self.context['request'].user)
        return company
