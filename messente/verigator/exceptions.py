class VerigatorError(Exception):
    def __init__(self, code, message):
        super(VerigatorError, self).__init__(message)
        self.code = code
        self.message = message


class InvalidDataError(VerigatorError):
    def __init__(self, code, message):
        super(InvalidDataError, self).__init__(code, message)


class NoSuchResourceError(VerigatorError):
    def __init__(self, code, message):
        super(NoSuchResourceError, self).__init__(code, message)


class ResourceAlreadyExistsError(VerigatorError):
    def __init__(self, code, message):
        super(ResourceAlreadyExistsError, self).__init__(code, message)


class ResourceForbiddenError(VerigatorError):
    def __init__(self, code, message):
        super(ResourceForbiddenError, self).__init__(code, message)


class WrongCredentialsError(VerigatorError):
    def __init__(self, code, message):
        super(WrongCredentialsError, self).__init__(code, message)


class InternalError(VerigatorError):
    def __init__(self, code, message):
        super(InternalError, self).__init__(code, message)


class InvalidResponseError(VerigatorError):
    def __init__(self, code, message):
        super(InvalidResponseError, self).__init__(code, message)