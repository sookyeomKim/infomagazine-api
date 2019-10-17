from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.utils import model_meta

from v1.company.models import Company
from v1.user.models import User, UserInfo, AccessRole


# class UserInfoSerializer(serializers.ModelSerializer):
#     organization = serializers.SerializerMethodField(read_only=True)
#     company = serializers.SerializerMethodField(read_only=True)
#
#     def get_organization(self, obj):
#         if obj.organization:
#             return model_to_dict(obj.organization)
#         else:
#             return None
#
#     def get_company(self, obj):
#         if obj.user.company_set.exists():
#             return [query_set for query_set in iter(
#                 obj.user.company_set.values('id', 'corp_name', 'corp_sub_name', 'corp_header', 'corp_address',
#                                             'corp_num',
#                                             'corp_desc').all()
#             )]
#         else:
#             return None
#
#     class Meta:
#         model = UserInfo
#         fields = ('access_role', 'phone_num', 'updated_date', 'organization', 'company',)

# class UserAuthReturnSerializer(serializers.ModelSerializer):
#     info = UserInfoSerializer(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'password', 'username', 'is_superuser', 'is_staff', 'is_active', 'info', 'last_login',
#                   'date_joined',)
#
#         extra_kwargs = {
#             'password':
#                 {
#                     'write_only': True
#                 },
#         }

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('access_role', 'phone_num', 'organization',)


class UserSerializer(serializers.ModelSerializer):
    info = UserInfoSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'info',)

        extra_kwargs = {
            'password':
                {
                    'write_only': True
                },
        }

    def validate(self, data):
        """
        1. 다른 유저의 정보는 수정할 수 없다.
        2. 관리자는 제외
        """

        if 'pk' in self.context:
            request_user = self.context['request'].user
            token_user_id = request_user.id
            request_user_id = int(self.context['pk'])
            if not request_user.is_staff and request_user.info.access_role is not 0:
                    if token_user_id is not request_user_id:
                        raise serializers.ValidationError("You can only edit your information.")
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        user_info_column = {
            'phone_num': validated_data['info']['phone_num']
        }
        UserInfo.objects.create(user=user, **user_info_column)

        return user

    def update(self, user_instance, validated_data):
        info = model_meta.get_field_info(user_instance)

        for attr, value in validated_data.items():
            if attr in info.relations:
                field = getattr(user_instance, attr)
                if info.relations[attr].to_many:
                    field.set(value)
                else:
                    for ono_attr, ono_value in value.items():
                        setattr(field, ono_attr, ono_value)
                    field.save()
            else:
                if attr == 'password':
                    user_instance.set_password(value)
                else:
                    setattr(user_instance, attr, value)

        user_instance.save()

        return user_instance


class CreateClientSerializer(UserSerializer):
    info = UserInfoSerializer()
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'info', 'company_id',)

        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }
        }

    def validate(self, data):
        """
        1. register_type이 company일 경우 반드시 company_id를 설정해야만 한다.
        2. 해당 company가 존재해야 한다.
        """
        if 'company_id' not in data:
            raise serializers.ValidationError("You must set 'company_id' in payload.")
        else:
            company_id = data['company_id']
            company_check = Company.objects.filter(id=company_id)
            if not company_check.exists():
                raise serializers.ValidationError("The company does not exist.")
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        user_info_column = {
            'user': user,
            'phone_num': validated_data['info']['phone_num']
        }
        request = self.context['request']
        user_info_column.update({'access_role': AccessRole.CLIENT,
                                 'organization': request.user.info.organization})
        UserInfo.objects.create(**user_info_column)

        company_id = validated_data['company_id']
        try:
            company = Company.objects.get(id=company_id)
            company.users.add(user)
        except ObjectDoesNotExist as e:
            user.delete()
            raise serializers.ValidationError(e)

        return user
