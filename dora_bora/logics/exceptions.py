class ServerNotFound(BaseException):
    pass


class InvalidVersion(BaseException):
    pass


class AccountNotFound(BaseException):
    pass


class InvalidAccountState(BaseException):
    pass


class InvalidWorldInfo(BaseException):
    pass


class NotHandled(BaseException):
    pass
