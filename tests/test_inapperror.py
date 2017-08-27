try:
    from unittest import mock
except ImportError:
    import mock

from pyinapp.appstore import AppStoreValidator


def test_include_response_on_status_error():
    response = {"status": 1}
    bundle_id = 'com.test.ok'

    with mock.patch('requests.post') as mock_post:
        mock_json = mock.Mock()
        mock_json.json.return_value = response
        mock_post.return_value = mock_json

        try:
            validator = AppStoreValidator(bundle_id).validate('')
        except Exception as e:
            assert e.response == response


def test_include_response_on_bundle_id_error():
    receipt = {"in_app":[], "bundle_id": "com.test.wrong"}
    response = {"status": 0, "in_app":[], "receipt": receipt}
    bundle_id = 'com.test.ok'

    with mock.patch('requests.post') as mock_post:
        mock_json = mock.Mock()
        mock_json.json.return_value = response
        mock_post.return_value = mock_json

        try:
            validator = AppStoreValidator(bundle_id).validate(receipt)
        except Exception as e:
            assert e.response == response


def test_include_response_on_bid_error():
    receipt = {"bid": "com.test.wrong"}
    response = {"status": 0, "in_app":[], "receipt": receipt}
    bundle_id = 'com.test.ok'

    with mock.patch('requests.post') as mock_post:
        mock_json = mock.Mock()
        mock_json.json.return_value = response
        mock_post.return_value = mock_json

        try:
            validator = AppStoreValidator(bundle_id).validate(receipt)
        except Exception as e:
            assert e.response == response
