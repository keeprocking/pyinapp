pyinapp
=======
|travis| |pypi|

.. |travis| image:: https://travis-ci.org/keeprocking/pyinapp.svg?branch=master
    :target: https://travis-ci.org/keeprocking/pyinapp
.. |pypi| image:: https://badge.fury.io/py/pyinapp.svg
    :target: https://badge.fury.io/py/pyinapp

In-app purchase validation has never been so friendly and convenient!

Installation
============
::

    pip install pyinapp

Usage
=====

Currently pyinapp supports Google Play and App Store receipts validation.

Google Play:
------------
.. code:: python

    from pyinapp import GooglePlayValidator, InAppValidationError


    bundle_id = 'com.yourcompany.yourapp'
    api_key = 'API key from the developer console'
    validator = GooglePlayValidator(bundle_id, api_key)

    try:
        purchases = validator.validate('receipt', 'signature')
        process_purchases(purchases)
    except InAppValidationError:
        """ handle validation error """

App Store:
----------
.. code:: python

    from pyinapp import AppStoreValidator, InAppValidationError


    bundle_id = 'com.yourcompany.yourapp'
    validator = AppStoreValidator(bundle_id)

    try:
        purchases = validator.validate('receipt')
        process_purchases(purchases)
    except InAppValidationError:
        """ handle validation error """

**Important!**
If your version is under 0.1.3, you need to check the type of purchases. For the sake of convenience you can process purchases this way:

.. code:: python

    def process_purchases(purchases):
        process(*purchases) if isinstance(purchases, list) else process(purchases)


    def process(*purchases):
        for p in purchases:
            """ for instance, save p to db and add a player some coins for it """


This approach allows to process both Google Play and App Store purchases the same way.

Purchase
========

Purchase is a universal wrapper for Google Play and App Store receipts. It contains the following fields:

- **transaction_id**: id of the purchase (**transaction_id** for App Store and **orderId** for Google Play);
- **product_id**: what product has been purchased (**product_id** for App Store and **productId** for Google Play);
- **quantity**: how many products have been purchased (**quantity** for App Store and always **1** for Google Play - there's no such field in Google Play receipt);
- **purchased_at**: when the product has been purchased, UNIX timestamp (**purchase_date** for App Store and **purchaseTime** for Google Play).
