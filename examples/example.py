"""
Flow as follows:
Create Service -> Create User -> Initiate Authentication -> Verify Pin
"""

from messente.verigator.api import Api

api = Api("username", "password")
service = api.services.create("http://example.com", "service_name")

user = api.users.create(service.id, "+xxxxxxxxxxx", "username")

auth_id = api.auth.initiate(service.id, user.id, api.auth.METHOD_SMS)

while True:
    try:
        input = raw_input  # Python 2 compatibility
    except NameError:
        pass

    token = input("Enter Sms Pin: ")
    auth_res, error = api.auth.verify(service.id, user.id, api.auth.METHOD_SMS, token, auth_id)

    if auth_res:
        break

    print("Not Verified... Reason: {}".format(error['result']))

print("Verified Successfully!")
