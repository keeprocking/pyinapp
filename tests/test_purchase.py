from pyinapp.purchase import Purchase


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
    assert purchase.response == None


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
    response = '["in_app":[]]'
    receipt = {
        'transaction_id': 1337,
        'product_id': 'pew pew',
        'purchase_date': '01.01.2016 12:00',
        'quantity': 100500,
    }
    purchase = Purchase.from_app_store_receipt(receipt, response)

    assert purchase.transaction_id == receipt['transaction_id']
    assert purchase.product_id == receipt['product_id']
    assert purchase.purchased_at == receipt['purchase_date']
    assert purchase.quantity == receipt['quantity']
    assert purchase.response == response
