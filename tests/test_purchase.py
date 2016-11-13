from pyinapp.purchase import Purchase
import pytest


def test_create_from_google_play_receipt():
    receipt = {
        'orderId': 1337,
        'productId': 'pew pew',
        'purchaseTime': '01.01.2016 12:00'
    }
    purchase = Purchase.from_google_play_receipt(receipt)

    assert purchase.transaction_id == receipt['orderId']
    assert purchase.product_id == receipt['productId']
    assert purchase.purchased_at == receipt['purchaseTime']
    assert purchase.quantity == 1


def test_create_from_test_google_play_receipt():
    receipt = {
        'purchaseToken': 1337,
        'productId': 'pew pew',
        'purchaseTime': '01.01.2016 12:00'
    }
    purchase = Purchase.from_google_play_receipt(receipt)

    assert purchase.transaction_id == receipt['purchaseToken']
    assert purchase.product_id == receipt['productId']
    assert purchase.purchased_at == receipt['purchaseTime']
    assert purchase.quantity == 1


def test_create_from_app_store_receipt():
    receipt = {
        'transaction_id': 1337,
        'product_id': 'pew pew',
        'purchase_date': '01.01.2016 12:00',
        'quantity': 100500
    }
    purchase = Purchase.from_app_store_receipt(receipt)

    assert purchase.transaction_id == receipt['transaction_id']
    assert purchase.product_id == receipt['product_id']
    assert purchase.purchased_at == receipt['purchase_date']
    assert purchase.quantity == receipt['quantity']