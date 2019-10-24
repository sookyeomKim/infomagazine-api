import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_enumfield import enum

from v1.organization.models import Organization


# TODO 수정하자!!
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
class User(AbstractUser):
    class Meta:
        db_table = 'user'

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{}".format(self.email)

    def get_access_role(self):
        return self.info.access_role


class AccessRole(enum.Enum):
    OWNER = 0
    MARKETER = 1
    CLIENT = 2
    GUEST = 3


# TODO 슈퍼 유저 생성 시 one to one 자동 생성되도록
# TODO null=True 없애라
class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='info')
    access_role = enum.EnumField(AccessRole, default=AccessRole.GUEST)
    organization = models.ForeignKey(Organization, default=None, null=True, on_delete=models.SET_NULL)
    phone_num = models.CharField(max_length=11)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_info'
