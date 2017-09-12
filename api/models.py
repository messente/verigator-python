class Service(object):
    def __init__(self, id, creation_time, name):
        self.id = id
        self.creation_time = creation_time
        self.name = name


class User(object):
    def __init__(self, id, creation_time, username):
        self.id = id
        self.creation_time = creation_time
        self.username = username
