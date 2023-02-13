class AlreadyExistsError(Exception):
    pass


class DatabaseError(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class AuthenticationFailedException(Exception):
    pass
