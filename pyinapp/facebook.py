from pyinapp.utils import decode_base64_url
from pyinapp.errors import InAppValidationError
import hmac
import hashlib
import json


class FacebookValidator(object):

    def __init__(self, secret):
        self.secret = secret

    def validate(self, signed_request):
        try:
            signature, payment_data, payload = self._decode_request(signed_request)
        except (TypeError, ValueError):
            raise InAppValidationError('Signature decoding error')

        expected_signature = hmac \
            .new(key=self.secret.encode(), msg=payload.encode(), digestmod=hashlib.sha256) \
            .digest()

        if signature != expected_signature:
            raise InAppValidationError('Signature mismatch')

        if payment_data['status'] != 'completed':
            raise InAppValidationError('Purchase is not completed')

        return payment_data['payment_id']

    def _decode_request(self, signed_request):
        signature, payload = signed_request.split('.')
        signature = decode_base64_url(signature)
        payment_data = decode_base64_url(payload).decode()
        payment_data = json.loads(payment_data)
        return signature, payment_data, payload
