from pyinapp.purchase import Purchase
from pyinapp.errors import InAppValidationError
from requests.exceptions import RequestException
import requests


api_result_ok = 0
api_result_errors = {
    21000: 'Bad json',
    21002: 'Bad data',
    21003: 'Receipt authentication',
    21004: 'Shared secret mismatch',
    21005: 'Server is unavailable',
    21006: 'Subscription has expired',
    21007: 'Sandbox receipt was sent to the production env',
    21008: 'Production receipt was sent to the sandbox env',
}


class AppStoreValidator(object):

    def __init__(self, bundle_id, sandbox=False):
        self.bundle_id = bundle_id

        if sandbox:
            self.url = 'https://sandbox.itunes.apple.com/verifyReceipt'
        else:
            self.url = 'https://buy.itunes.apple.com/verifyReceipt'

    def validate(self, receipt, password=None):
        receipt_json = {'receipt-data': receipt}
        if password:
            receipt_json['password'] = password

        try:
            api_response = requests.post(self.url, json=receipt_json).json()
        except (ValueError, RequestException):
            raise InAppValidationError('HTTP error')

        status = api_response['status']

        if status != api_result_ok:
            error = InAppValidationError(api_result_errors.get(status, 'Unknown API status'), api_response)
            raise error

        receipt = api_response['receipt']
        purchases = self._parse_receipt(receipt, api_response)
        return purchases

    def _parse_receipt(self, receipt, response):
        if 'in_app' in receipt:
            return self._parse_ios7_receipt(receipt, response)
        return self._parse_ios6_receipt(receipt, response)

    def _parse_ios6_receipt(self, receipt, response):
        if self.bundle_id != receipt['bid']:
            error = InAppValidationError('Bundle id mismatch', response)
            raise error
        return [Purchase.from_app_store_receipt(receipt, response)]

    def _parse_ios7_receipt(self, receipt, response):
        if self.bundle_id != receipt['bundle_id']:
            error = InAppValidationError('Bundle id mismatch', response)
            raise error
        return [Purchase.from_app_store_receipt(r, response) for r in receipt['in_app']]
