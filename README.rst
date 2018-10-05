Verigator Python Library
========================

|Build Status|

Easy to use Python (2.7 and 3) wrapper for verigator rest api.

Installing
~~~~~~~~~~

The library can be installed from pip:

::

    pip install verigator

Or you can build it manually:

::

    git clone https://github.com/messente/verigator-python.git

    cd verigator-python

    python setup.py install

::

Documentation
~~~~~~~~~~~~~

detailed docs can be found `here`_

Examples
~~~~~~~~

.. code:: python

    from messente.verigator.api import Api

    # initialize api
    api = Api("username", "password")

    # create example service
    service = api.services.create("http://example.com", "service_name")

    # add user to the created service
    user = api.users.create(service.id, "+xxxxxxxxxxx", "username")

    # initiate sms authentication, you can use api.auth.METHOD_TOTP for time
    api.auth.initiate(service.id, user.id, api.auth.METHOD_SMS)

    # check user input until successfull pin verification
    while True:
        try:
            input = raw_input  # Python 2 compatibility
        except NameError:
            pass

        # read user input
        token = input("Enter Sms Pin: ")

        # verify pin
        verified = api.auth.verify(service.id, user.id, token)

        if verified:
            break

        print("Not Verified...")

    print("Verified Successfully!")

License
~~~~~~~

This project is licensed under the Apache License 2.0 - see the
`LICENSE.txt`_ file for details

.. _here: https://messente.github.io/verigator-python/modules.html
.. _LICENSE.txt: LICENSE.txt

.. |Build Status| image:: https://travis-ci.org/messente/verigator-python.svg?branch=master
   :target: https://travis-ci.org/messente/verigator-python