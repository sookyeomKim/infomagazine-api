from django.db import models
from v1.user.models import User


# Create your models here.


class Company(models.Model):
    users = models.ManyToManyField(User)
    corp_name = models.CharField(max_length=100, unique=True)
    corp_sub_name = models.CharField(max_length=100, blank=True)
    corp_header = models.CharField(max_length=20, blank=True)
    corp_address = models.CharField(max_length=200, blank=True)
    corp_num = models.CharField(max_length=50, blank=True)
    corp_desc = models.CharField(max_length=200, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.corp_name
