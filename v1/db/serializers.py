from rest_framework import serializers

from v1.db.models import LandingPageDB


class LandingPageDBSerializer(serializers.ModelSerializer):
    db = serializers.SerializerMethodField()

    def get_db(self, obj):
        result = {}
        for key, val in obj.data.items():
            result[obj.schema[key]] = val
            result.update(result)
        return result

    class Meta:
        model = LandingPageDB
        fields = ('id',
                  'landing_id',
                  'db',
                  'user_agent',
                  'ip_v4_address',
                  'inflow_path',
                  'stay_time',
                  'registered_date',
                  )
        extra_kwargs = {
            'registered_date': {
                'read_only': True
            }
        }
