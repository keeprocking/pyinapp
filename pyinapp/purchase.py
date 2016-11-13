
class Purchase(object):

    def __init__(self, transaction_id, product_id, quantity, purchased_at):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.purchased_at = purchased_at

    @classmethod
    def from_app_store_receipt(cls, receipt):
        purchase = {
            'transaction_id': receipt['transaction_id'],
            'product_id': receipt['product_id'],
            'quantity': receipt['quantity'],
            'purchased_at': receipt['purchase_date']
        }
        return cls(**purchase)

    @classmethod
    def from_google_play_receipt(cls, receipt):
        purchase = {
            'transaction_id': receipt.get('orderId', receipt.get('purchaseToken')),
            'product_id': receipt['productId'],
            'quantity': 1,
            'purchased_at': receipt['purchaseTime']
        }
        return cls(**purchase)
