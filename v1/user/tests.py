"""
유저 관련 테스트케이스
"""

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from v1.company.models import Company
from v1.organization.models import Organization
from v1.user.models import User, AccessRole


class UserRegistrationAPITestCase(APITestCase):
    """
    1. 이메일 체크
    2. 유저 등록
    3. 이메일 확인 후 유저 등록
    4. 유저 인증
    5. 유저 부분 업데이트
    6. 마케터 계정 생성
    7. 고객 생성
    """
    user_list_url = reverse('v1:router:user-list')
    user_email_check_url = reverse('v1:router:user-email-check')
    user_create_client_url = reverse('v1:router:user-create-client')

    obtain_token_url = reverse('v1:token_obtain_sliding')

    def setUp(self):
        self.user_data = {
            'email': 'testcase@lcventures.kr',
            'username': 'testcase',
            'password': 'testcase',
            'info':
                {
                    'phone_num': '01099991111'
                }
        }

    def test_user_email_check(self, duplicate_check=False, email=None):
        """
        이메일 체크

        1. qs에 email을 추가하지 않았을 때
        2. qs에 email을 추가했을 때
        """
        if not email:
            email = self.user_data['email']

        # 1
        response = self.client.get(self.user_email_check_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], False)

        # 2
        response = self.client.get(self.user_email_check_url + '?email=' + email)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], True)

        if duplicate_check:
            self.assertEqual(response.data['data']['email_check'], True)
        else:
            self.assertEqual(response.data['data']['email_check'], False)

    def test_user_registration(self, user_data=None, fail_check=False, return_value=False):
        """
        유저 등록

        **kwargs
        user_data, 등록 테스트할 유저 데이터를 명시한다. 기본은 self.user_data

        fail_check = False, 성공 여부를 판단
        fail_check = True, 실패 여부를 판단

        return_value = False, 유저 등록의 응답을 미반환
        return_value = True, 유저 등록의 응답을 반환
        """
        if not user_data:
            user_data = self.user_data

        response = self.client.post(self.user_list_url, user_data)

        if not fail_check:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        if return_value:
            return response

    def test_user_registration_with_unique_email_validation(self):
        """
        이메일 확인 후 유저 등록

        1. 유저 등록
        2. 동일 정보로 이메일 체크 > 중복
        3. 동일 정보로 유저 등록 > 실패
        4. 새로운 이메일 체크 > 없음
        5. 새로운 정보로 유저 등록 > 성공
        """

        # 1
        self.test_user_registration()

        duplicate_user_data = self.user_data

        # 2
        self.test_user_email_check(email=duplicate_user_data['email'], duplicate_check=True)

        # 3
        self.test_user_registration(user_data=duplicate_user_data, fail_check=True)

        new_email = duplicate_user_data['email'] + 'dummy'

        # 4
        self.test_user_email_check(email=new_email)

        new_user_data = duplicate_user_data.update({'email': new_email})

        # 5
        self.test_user_registration(user_data=new_user_data)

    def test_user_auth(self, user_data=None):
        """
        유저 인증

        1. 유저 등록
        2. 토큰 생성 > 실패
        3. 토큰 생성 > 성공
        """
        # 1
        result = {}
        if not user_data:
            user_data = self.user_data
            response = self.test_user_registration(return_value=True)
            result['user_id'] = response.data['data']['id']
        else:
            result['user_id'] = user_data['user_id']

        # 2
        response = self.client.post(self.obtain_token_url,
                                    {'email': user_data['email'],
                                     'password': user_data['password'] + 'dummy'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 3
        response = self.client.post(self.obtain_token_url,
                                    {'email': user_data['email'],
                                     'password': user_data['password']},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

        result['token'] = response.data['token']

        return result

    def test_user_partial_update(self, auth=None, target=None, data=None):
        """
        유저 부분 업데이트

        1. 토큰 생성
        2. 신규 유저 생성
        3. 다른 유저의 정보 변경 시도 > 실패
        4. 본인 정보 변경 시도 > 성공
        """
        if not auth:
            auth = self.test_user_auth()
        if not target:
            target = auth
        if not data:
            data = {'info': {'phone_num': '01088882222'}}

        # 1
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth['token'])

        # 2
        user_data = self.user_data.update({'email': 'testcase' + str(auth['user_id']) + '@lcventures.kr'})
        response = self.test_user_registration(user_data=user_data, return_value=True)

        # 3
        get_user_data = User.objects.select_related('info').values('is_staff', 'info__access_role').get(
            id=auth['user_id'])
        if not get_user_data['is_staff'] and get_user_data['info__access_role'] is not 0:
            response = self.client.patch(reverse('v1:router:user-detail', kwargs={'pk': response.data['data']['id']}),
                                         data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # 4
            response = self.client.patch(reverse('v1:router:user-detail', kwargs={'pk': target['user_id']}),
                                         data=data)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            response = self.client.patch(reverse('v1:router:user-detail', kwargs={'pk': target['user_id']}),
                                         data=data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_marketer_registration(self):
        """
        마케터 계정 생성

        1. 조직 생성
        2. 게스트 계정 생성 및 인증
        3. 마케터 신청(조직 적용)
        4. 오너 계정 생성 및 인증
        5. 마케터 신청 계정 권한 변경
        """
        # 1
        organization, create = Organization.objects.get_or_create(org_name='sibal')

        marketer_data = self.user_data.copy()
        marketer_data.update({'email': 'marketer@lcventures.kr'})
        response = self.test_user_registration(user_data=marketer_data, return_value=True)
        marketer_data.update({'user_id': response.data['data']['id']})
        marketer_auth = self.test_user_auth(user_data=marketer_data)

        # 2
        self.test_user_partial_update(auth=marketer_auth, data={'info': {'organization': organization.id}})

        # 3
        owner_data = self.user_data.copy()
        owner_data.update({'email': 'owner@lcventures.kr'})
        response = self.test_user_registration(user_data=owner_data, return_value=True)
        owner_data.update({'user_id': response.data['data']['id']})
        get_user_data = User.objects.get(id=owner_data['user_id'])
        get_user_data.info.access_role = AccessRole.OWNER
        get_user_data.info.save()

        # 4
        owner_auth = self.test_user_auth(user_data=owner_data)

        # 5
        self.test_user_partial_update(auth=owner_auth, target=marketer_auth,
                                      data={'info': {'access_role': AccessRole.MARKETER}})

        return marketer_auth

    def test_client_registration(self):
        """
        고객 생성

        1. 업체 생성
        2. 고객 생성
        """

        # 1
        company, create = Company.objects.get_or_create(corp_name='sisisisibal')

        marketer_auth = self.test_marketer_registration()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + marketer_auth['token'])

        # 2
        client_data = self.user_data.copy()
        client_data.update({'email': 'client@lcventures.kr'})
        client_data.update({'company_id': company.id})
        response = self.client.post(self.user_create_client_url, client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access_role_check = User.objects.select_related('info') \
            .values('info__access_role') \
            .get(id=response.data['data']['id'])['info__access_role']
        self.assertEqual(access_role_check, 2)
        user_company_check = Company.objects.prefetch_related('users').filter(users__id=response.data['data']['id'])