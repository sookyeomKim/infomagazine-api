from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

import v1.permissions as custom_permissions
from infomagazine.custom_packages import CustomModelViewSet
from v1.user.filters import UserFilter
from v1.user.models import User
from v1.user.serializers import UserSerializer, CreateClientSerializer


class UserViewSets(CustomModelViewSet):
    queryset = User.objects.select_related('info').all()
    serializer_class = UserSerializer
    filterset_class = UserFilter

    # @action(detail=False, methods=['GET'])
    # def csrf(self, request):
    #     csrf.get_token(request)
    #     return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def authInfo(self, request):
        """
        2019/10/21

        인증된 토큰의 유저 정보를 반환 받는다.

        :param request:
        :return:
        """
        result = {
            'state': True,
            'data': {
                'id': request.user.pk,
                'email': request.user.email,
                'username': request.user.username,
                'access_role': request.user.info.access_role,
                'is_staff': request.user.is_staff
            },
            'message': 'success'
        }
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def create_client(self, request):
        serializer = CreateClientSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        result = {
            'state': True,
            'data': serializer.data,
            'message': 'success'
        }

        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['GET'])
    def email_check(self, request):
        get_qs = request.query_params.dict()
        result = {
            'state': False,
            'data':
                {
                    'email_check': False
                },
            'message': 'fail'
        }

        if 'email' not in get_qs:
            result['message'] = 'must set query string "email"'
        else:
            result['state'] = True
            email_check = User.objects.filter(email=get_qs['email'])

            if email_check.exists():
                result['data']['email_check'] = True
                result['message'] = 'Existing email.'
            else:
                result['message'] = 'Nonexistent email.'

        return Response(result, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['list', 'create_client', 'destroy']:
            permission_classes = [custom_permissions.IsMarketer]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'email_check', 'csrf']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['authInfo']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

        if self.action in ['update', 'partial_update'] and 'pk' in self.kwargs:
            context.update({'pk': self.kwargs['pk']})

        return context
