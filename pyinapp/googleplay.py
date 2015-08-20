from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from pyinapp.errors import InAppValidationError
from pyinapp.purchase import Purchase
import base64
import json

purchase_state_ok = 0


class GooglePlayValidator(object):

    def __init__(self, bundle_id, api_key):
        self.bundle_id = bundle_id
        self.public_key = RSA.importKey(base64.standard_b64decode(api_key))

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

            purchase = {
                'transaction_id': receipt_json['orderId'],
                'product_id': receipt_json['productId'],
                'quantity': 1,
                'purchased_at': receipt_json['purchaseTime']
            }
            return Purchase(**purchase)
        except (KeyError, ValueError):
            raise InAppValidationError('Bad receipt')

    def _validate_signature(self, receipt, signature):
        try:
            encoded_receipt = receipt.encode()
            sha = SHA.new(encoded_receipt)
            verifier = PKCS1_v1_5.new(self.public_key)
            signature = base64.standard_b64decode(signature)
            return verifier.verify(sha, signature)
        except (TypeError, ValueError):
            return False
