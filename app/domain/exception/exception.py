from app.domain.exception.error_code import ErrorCode

class BusinessException(Exception):

    def __init__(self, error_code: ErrorCode, *args):
        self.error_code = error_code
        self.args = args

    def get_error_code(self) -> str:
        return self.error_code.code

    def get_error_message(self) -> str:
        if self.args:
            return self.error_code.description.format(*self.args)
        else:
            return self.error_code.description
