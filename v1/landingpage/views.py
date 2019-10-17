import time
import boto3

from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.response import Response

import v1.permissions as custom_permissions
from infomagazine.utils import response_decorator

from v1.company.models import Company
from v1.landingpage.models import LandingPage as LandingModel
from v1.landingpage.utils import LandingPage as LandingGenerator
from v1.user.models import AccessRole


class _LandingPageViewSetsUtils(viewsets.ViewSet):
    landing_pages_model = LandingModel(choice_db='infomagazine')
    permission_classes = (custom_permissions.IsMarketer,)

    def _get_landing_data(self, landing_detail=None, is_generate=False):
        if landing_detail['state']:
            landing_pages = LandingGenerator(landing_detail['data']['landing_info'], is_generate=is_generate)
            lading_page_generated = landing_pages.generate()
            lading_page_generated.update(
                {'options': {'status': status.HTTP_200_OK} if landing_detail['state'] else {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR}})

            return lading_page_generated
        else:
            landing_detail.update({'options': {'status': status.HTTP_200_OK} if landing_detail['state'] else {
                'status': status.HTTP_404_NOT_FOUND}})

            return landing_detail

    def _cf_inv_request(self, session, url):
        """
        2019/08/26

        :param session:
        :param url:
        :return:
        """
        epoch_time = time.time()
        cf_inv_response_data = session.create_invalidation(
            DistributionId=getattr(settings, 'CF_DISTRIBUTION_ID'),
            InvalidationBatch={
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        url,
                    ]
                },
                'CallerReference': str(int(epoch_time))
            }
        )
        if cf_inv_response_data['ResponseMetadata']['HTTPStatusCode'] == 201:
            return {'state': True, 'data': url, 'message': 'Succeed.',
                    'options': {'status': status.HTTP_200_OK}}
        else:
            return {'state': False, 'data': '', 'message': 'Failed.',
                    'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}

    def get_permissions(self):
        permission_classes = [custom_permissions.IsClient]
        return [permission() for permission in permission_classes]


class LandingPageViewSets(_LandingPageViewSetsUtils):
    @response_decorator
    def list(self, request, *args, **kwargs):
        projection = {'_id': 1, 'landing_info.landing.name': 1, 'landing_info.landing.views': 1}
        if not request.user.is_staff:
            filter_fields = {
                'users__info__organization_id': request.user.info.organization_id,
            }
            if request.user.info.access_role == AccessRole.CLIENT:
                filter_fields.update({'users__id': request.user.id})
            users_rel_comp_id = Company.objects.filter(**filter_fields).values("id").distinct()
            users_rel_comp_id_list = [item['id'] for item in users_rel_comp_id]
            query_option = {"company_id": {"$in": users_rel_comp_id_list}}
            response_data = self.landing_pages_model.list(choice_collection='landing_pages', query=query_option,
                                                          projection=projection)
        else:
            response_data = self.landing_pages_model.list(choice_collection='landing_pages', projection=projection)
        response_data.update({"options": {'status': status.HTTP_200_OK} if response_data['state'] else {
            'status': status.HTTP_404_NOT_FOUND}})
        return response_data

    @response_decorator
    def create(self, request):
        document = {
            "company_id": request.data['company_id'],
            "landing_info": request.data['landing_info'],
            "updated_date": request.data['updated_date']
        }
        response_data = self.landing_pages_model.create(choice_collection='landing_pages', document=document)
        response_data.update({"options": {'status': status.HTTP_201_CREATED} if response_data['state'] else {
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR}})

        return response_data

    @response_decorator
    def retrieve(self, request, pk):
        response_data = self.landing_pages_model.retrieve(choice_collection='landing_pages', doc_id=pk)
        response_data.update({"options": {'status': status.HTTP_200_OK} if response_data['state'] else {
            'status': status.HTTP_404_NOT_FOUND}})
        return response_data

    @response_decorator
    def update(self, request, pk):
        response_data = self.landing_pages_model.update(choice_collection='landing_pages', doc_id=pk,
                                                        data_to_update={'$set': request.data})
        response_data.update({"options": {'status': status.HTTP_200_OK} if response_data['state'] else {
            'status': status.HTTP_404_NOT_FOUND}})
        return response_data

    @response_decorator
    def destroy(self, request, pk):
        response_data = self.landing_pages_model.destroy(choice_collection='landing_pages', doc_id=pk)
        response_data.update({"options": {'status': status.HTTP_204_NO_CONTENT} if response_data['state'] else {
            'status': status.HTTP_404_NOT_FOUND}})
        return response_data

    @action(detail=True)
    @response_decorator
    def preview(self, request, pk):
        get_detail = self.retrieve(request, pk)
        response_data = self._get_landing_data(landing_detail=get_detail.data)
        return response_data

    @action(detail=True, renderer_classes=[StaticHTMLRenderer], permission_classes=[permissions.AllowAny])
    def test_preview(self, request, pk):
        get_detail = self.retrieve(request, pk)
        response_data = self._get_landing_data(landing_detail=get_detail.data)
        return Response(response_data['data'])

    @action(detail=True, methods=['GET', 'POST', 'PUT'])
    @response_decorator
    def landing_urls(self, request, pk):
        """
        2019/08/26

        :param request:
        :param pk:

        """
        session = boto3.session.Session(aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
                                        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'),
                                        region_name='ap-northeast-2')
        s3_client = session.client('s3')
        cloudfront_client = session.client('cloudfront')

        if request.method == 'GET':
            s3_response = s3_client.list_objects(Bucket=getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                                                 Prefix='landings/' + pk + '/')
            if s3_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                url_list_do_handling = [url['Key'].replace('landings/', 'https://landings.infomagazine.xyz/') for url in
                                        s3_response.get('Contents', []) if url]
                return {'state': True, 'data': url_list_do_handling, 'message': 'Succeed.',
                        'options': {'status': status.HTTP_200_OK}}
            else:
                return {'state': False, 'data': '', 'message': 'Failed.',
                        'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}

        elif request.method == 'POST':
            get_detail = self.retrieve(request, pk)
            response_data = self._get_landing_data(landing_detail=get_detail.data, is_generate=True)

            if response_data['state']:
                landing_base_url = get_detail.data['data']['landing_info']['landing']['base_url']
                epoch_time = time.time()
                landing_url = f'''landings/{pk}/{landing_base_url}_{str(int(epoch_time))}.html'''
                s3_response_data = s3_client.put_object(Body=response_data['data'],
                                                        Bucket=getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                                                        Key=landing_url,
                                                        ContentType='text/html')
                if s3_response_data['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return {'state': True, 'data': landing_url, 'message': 'Succeed.',
                            'options': {'status': status.HTTP_201_CREATED}}
                else:
                    return {'state': False, 'data': '', 'message': 'Failed.',
                            'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}
            else:
                return {'state': response_data['state'], 'data': response_data['data'],
                        'message': response_data['message'],
                        'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}
        elif request.method == 'PUT':
            return self._cf_inv_request(session=cloudfront_client, url=f'''/{pk}/''')

    @action(detail=True, methods=['PUT', 'DELETE'], url_path='landing_urls/(?P<landing_url>[^/.]+)')
    @response_decorator
    def landing_urls_detail(self, request, pk, landing_url):
        """
        2019/08/26

        :param request:
        :param pk:
        :param landing_url:

        """
        session = boto3.session.Session(aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID'),
                                        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY'),
                                        region_name='ap-northeast-2')
        s3_client = session.client('s3')
        cloudfront_client = session.client('cloudfront')
        if request.method == 'PUT':
            get_detail = self.retrieve(request, pk)
            response_data = self._get_landing_data(landing_detail=get_detail.data, is_generate=True)
            if response_data['state']:
                s3_response_data = s3_client.put_object(Body=response_data['data'],
                                                        Bucket=getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                                                        Key=f'''landings/{pk}/{landing_url}.html''',
                                                        ContentType='text/html')
                if s3_response_data['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return self._cf_inv_request(session=cloudfront_client, url=f'''/{pk}/{landing_url}.html''')
                else:
                    return {'state': False, 'data': '', 'message': 'Failed.',
                            'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}
            else:
                return {'state': response_data['state'], 'data': response_data['data'],
                        'message': response_data['message'],
                        'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}
        elif request.method == 'DELETE':
            s3_response = s3_client.delete_object(Bucket=getattr(settings, 'AWS_STORAGE_BUCKET_NAME'),
                                                  Key='landings/' + pk + '/' + landing_url + '.html')
            if s3_response['ResponseMetadata']['HTTPStatusCode'] == 204:
                return {'state': True, 'data': landing_url, 'message': 'Succeed.',
                        'options': {'status': status.HTTP_204_NO_CONTENT}}
            else:
                return {'state': False, 'data': '', 'message': 'Failed.',
                        'options': {'status': status.HTTP_500_INTERNAL_SERVER_ERROR}}
