class IQSuiteException(Exception):
    """Base exception for IQSuite SDK"""
    pass

class AuthenticationError(IQSuiteException):
    """Raised when authentication fails"""
    pass

class APIError(IQSuiteException):
    """Raised when the API returns an error"""
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response