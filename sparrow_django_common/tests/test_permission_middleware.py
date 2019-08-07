import unittest
from unittest import mock


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:9999/api':
        return MockResponse({"status": True, "message": "成功", }, 200)
    return MockResponse({"status": False, "message": "失败"}, 200)


class TestPermissionMiddleware(unittest.TestCase):
    """测试permission_middleware"""

    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.verify_middleware_location',
                return_value='')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.valid_permission_svc',
                return_value='')
    @mock.patch('django.conf.settings', return_value='')
    @mock.patch('sparrow_django_common.utils.normalize_url.NormalizeUrl.normalize_url',
                return_value='http://127.0.0.1:9999/api')
    def test_have_authority(self, NormalizeUrl, settings, valid_permission_svc, requests, verify_middleware_location):
        from sparrow_django_common.middleware.permission_middleware import PermissionMiddleware
        self.assertEqual(PermissionMiddleware().has_permission(requests, view=''), True)

    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.verify_middleware_location',
                return_value='')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('sparrow_django_common.utils.validation_data.VerificationConfiguration.valid_permission_svc',
                return_value='')
    @mock.patch('django.conf.settings', return_value='')
    @mock.patch('sparrow_django_common.utils.normalize_url.NormalizeUrl.normalize_url',
                return_value='http://127.0.0.1:9d999/api')
    def test_no_permission(self, NormalizeUrl, settings, valid_permission_svc, requests, verify_middleware_location):
        from sparrow_django_common.middleware.permission_middleware import PermissionMiddleware
        self.assertEqual(PermissionMiddleware().has_permission(requests, view=''), False)


if __name__ == '__main__':
    unittest.main()
