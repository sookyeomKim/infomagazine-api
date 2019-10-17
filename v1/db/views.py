import v1.permissions as custom_permissions
from infomagazine.custom_packages import CustomModelViewSet
from v1.db.filters import DBFilter
from v1.db.models import LandingPageDB
from v1.db.serializers import LandingPageDBSerializer


class LandingPageDBViewSets(CustomModelViewSet):
    filterset_class = DBFilter
    serializer_class = LandingPageDBSerializer

    def get_queryset(self):
        return LandingPageDB.objects.filter(landing_id=self.kwargs['landing_page_pk'])

    # def get_queryset(self):
    #     if self.request.method == 'GET':
    #         request = self.request
    #
    #         get_qs = request.query_params.dict()
    #
    #         filter_fields = {
    #             'users__info__organization_id': request.user.info.organization_id,
    #             'users__info__access_role__in': [0, 1]
    #         }
    #
    #         if 'detail' in get_qs:
    #             del get_qs['detail']
    #             filter_fields.update({'users__id': request.user.id})
    #
    #         filter_fields.update({key + "__contains": value for key, value in get_qs.items()})
    #
    #         return self.queryset.filter(**filter_fields)
    #     return self.queryset.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [custom_permissions.IsClient]
        else:
            permission_classes = [custom_permissions.IsMarketer]

        return [permission() for permission in permission_classes]
