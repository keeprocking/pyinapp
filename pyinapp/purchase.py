
class Purchase(object):

    def __init__(self, transaction_id, product_id, quantity, purchased_at):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.purchased_at = purchased_at
