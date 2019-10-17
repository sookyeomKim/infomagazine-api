from django.db import models
from django_mysql.models import JSONField
from django.core.validators import MinLengthValidator


class LandingPageDB(models.Model):
    landing_id = models.CharField(max_length=24, validators=[MinLengthValidator(24)])
    data = JSONField()
    schema = JSONField()
    user_agent = JSONField()
    ip_v4_address = models.CharField(blank=True, max_length=19, validators=[MinLengthValidator(19)])
    inflow_path = models.CharField(blank=True, max_length=256)
    stay_time = models.CharField(blank=True, max_length=10)
    registered_date = models.CharField(max_length=13)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'landing_page_db'
        ordering = ('-registered_date',)
