from pyinapp.errors import InAppValidationError
from pyinapp.purchase import Purchase
import base64
import json
import rsa


purchase_state_ok = 0


def make_pem(public_key):
    return '\n'.join((
        '-----BEGIN PUBLIC KEY-----',
        '\n'.join(public_key[i:i+64] for i in range(0, len(public_key), 64)),
        '-----END PUBLIC KEY-----'
    ))


class GooglePlayValidator(object):

    def __init__(self, bundle_id, api_key):
        self.bundle_id = bundle_id
        pem = make_pem(api_key)
        self.public_key = rsa.PublicKey.load_pkcs1_openssl_pem(pem)

    def validate(self, receipt, signature):
        ok = self._validate_signature(receipt, signature)

        if not ok:
            raise InAppValidationError('Bad signature')

        try:
            receipt_json = json.loads(receipt)

            if receipt_json['packageName'] != self.bundle_id:
                raise InAppValidationError('Bundle id mismatch')

            if receipt_json['purchaseState'] != purchase_state_ok:
                raise InAppValidationError('Item is not purchased')

            return Purchase.from_google_play_receipt(receipt_json)
        except (KeyError, ValueError):
            raise InAppValidationError('Bad receipt')

    def _validate_signature(self, receipt, signature):
        try:
            sig = base64.standard_b64decode(signature)
            return rsa.verify(receipt.encode(), sig, self.public_key)
        except rsa.VerificationError:
            return False

