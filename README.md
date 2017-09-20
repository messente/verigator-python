# Verigator Python Library
[![Build Status](https://travis-ci.org/messente/verigator-python.svg?branch=master)](https://travis-ci.org/messente/verigator-python)

Easy to use Python (2.7 and 3) wrapper for verigator rest api.

### Installing

The library can be installed from pip:

```
pip install verigator
```
Or you can build it manually:

```
git clone https://github.com/messente/verigator-python.git

cd verigator-python

python setup.py install
```
Check installation
```
$ python -c "from messente.verigator import __version__;print(__version__)"

0.0.1
```

## Documentation

detailed docs can be found [here](http://example.com)

## Examples
```Python
from messente.verigator.api import Api

# initialize api
api = Api("username", "password")

# create example service
service = api.services.create("http://example.com", "service_name")

# add user to the created service
user = api.users.create(service.id, "+xxxxxxxxxxx", "username")

# initiate sms authentication.
# you can use api.auth.METHOD_TOTP for time-based one-time password authentication
auth_id = api.auth.initiate(service.id, user.id, api.auth.METHOD_SMS)

# check user input until successfull pin verification
while True:
    try:
        input = raw_input  # Python 2 compatibility
    except NameError:
        pass

    # read user input
    token = input("Enter Sms Pin: ")
    
    #verify pin
    verified, error = api.auth.verify(service.id, user.id, api.auth.METHOD_SMS, token, auth_id)

    if verified:
        break

    print("Not Verified... Reason: {}".format(error['result']))

print("Verified Successfully!")

```
## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.txt](LICENSE.txt) file for details
