import random
import string

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from contents.datalayers.content import ContentDataLayer
from users.datalayers import UserDataLayer
from backend.settings import REST_FRAMEWORK


class ContentTestCase(TestCase):

    @classmethod
    def create_title_body(cls):
        title = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(50)])
        body = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(1000)])

        return title, body

    @classmethod
    def create_single_text_field(cls):
        return dict(
            name="sub_title", field_type="basic",
            value="".join([random.choice(string.ascii_letters + string.digits) for _ in range(100)])
        )

    def obtain_jwt_token(self, username, password='12345'):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={'username': username, 'password': password}
        )

        return f'JWT {response.data["access"]}'

    @classmethod
    def setUpTestData(cls):
        for i in range(3):
            title, body = cls.create_title_body()
            username, password = f'test{i}', '12345'
            editor = UserDataLayer.create_user(username=username, email=f'{username}@test.com', password=password)
            ContentDataLayer.create_content(title=title, body=body, author=editor)

    def test_logging_in(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={'username': 'test1', 'password': '12345'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_getting_content_list_without_authentication(self):
        response = self.client.get(
            reverse('contents:api:v1:content_api_view')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_content_list_with_authentication(self):
        test1_authorization = self.obtain_jwt_token('test1')
        response = self.client.get(
            reverse('contents:api:v1:content_api_view'),
            HTTP_AUTHORIZATION=test1_authorization
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creating_content_without_authentication(self):
        title, body = self.create_title_body()

        response = self.client.post(
            reverse('contents:api:v1:content_api_view'),
            data={'title': title, 'body': body}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creating_content_with_authentication(self):
        test1_authorization = self.obtain_jwt_token('test1')
        title, body = self.create_title_body()

        response = self.client.post(
            reverse('contents:api:v1:content_api_view'),
            data={'title': title, 'body': body},
            HTTP_AUTHORIZATION=test1_authorization
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_getting_single_content_without_authentication(self):
        response = self.client.get(
            reverse('contents:api:v1:content_details_api_view', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_single_content_with_authentication(self):
        test1_authorization = self.obtain_jwt_token('test1')
        response = self.client.get(
            reverse('contents:api:v1:content_details_api_view', kwargs={'pk': 1}),
            HTTP_AUTHORIZATION=test1_authorization
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_changing_own_content(self):
        test1_authorization = self.obtain_jwt_token('test1')
        title, body = self.create_title_body()

        response = self.client.post(
            reverse('contents:api:v1:content_api_view'),
            data={'title': title, 'body': body},
            HTTP_AUTHORIZATION=test1_authorization
        )

        title, body = self.create_title_body()
        response = self.client.patch(
            reverse('contents:api:v1:content_details_api_view', args=[response.data.get('id')]),
            data={'title': title, 'body': body}, content_type='application/json',
            HTTP_AUTHORIZATION=test1_authorization
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_changing_content_of_other(self):
        test1_authorization, test2_authorization = self.obtain_jwt_token('test1'), self.obtain_jwt_token('test2')
        title, body = self.create_title_body()

        response = self.client.post(
            reverse('contents:api:v1:content_api_view'),
            data={'title': title, 'body': body},
            HTTP_AUTHORIZATION=test1_authorization
        )

        title, body = self.create_title_body()
        response = self.client.patch(
            reverse('contents:api:v1:content_details_api_view', args=[response.data.get('id')]),
            data={'title': title, 'body': body}, content_type='application/json',
            HTTP_AUTHORIZATION=test2_authorization
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_throttling_get_request(self):
        throttle_rates = REST_FRAMEWORK.get('DEFAULT_THROTTLE_RATES')
        if throttle_rates:
            anon, user = throttle_rates.get('anon', None), throttle_rates.get('user', None)
            anon_rate = int(anon.split('/')[0]) if anon else None
            user_rate = int(user.split('/')[0]) if user else None
        else:
            anon_rate, user_rate = None, None

        if anon_rate:
            response = None
            for i in range(anon_rate+1):
                response = self.client.get(
                    reverse('contents:api:v1:content_details_api_view', kwargs={'pk': 1})
                )

            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        if user_rate:
            response = None
            for i in range(user_rate+1):
                response = self.client.get(
                    reverse('contents:api:v1:content_details_api_view', kwargs={'pk': 1})
                )

            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_creating_content_with_dynamic_text_fields(self):
        test1_authorization = self.obtain_jwt_token('test1')
        title, body = self.create_title_body()
        dynamic_text_fields = [self.create_single_text_field(), self.create_single_text_field()]

        response = self.client.post(
            reverse('contents:api:v1:content_api_view'),
            data={'title': title, 'body': body, 'dynamic_text_fields': dynamic_text_fields},
            HTTP_AUTHORIZATION=test1_authorization
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
