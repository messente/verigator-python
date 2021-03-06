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
