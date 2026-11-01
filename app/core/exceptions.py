class AppException(Exception):
    status_code = 400
    default_detail = "An application error occurred"
    
    def __init__(self, detail: str | None = None):
        self.detail = (detail if detail is not None else self.default_detail)
        super().__init__(self.detail)
        
class InvalidTokenError(AppException):
    status_code = 401
    default_detail = "Invalid or expired tiken."
    
class CredentialError(AppException):
    status_code = 401
    default_detail = "Invalid credentials."
    
class UserAlreadyExistsError(AppException):
    status_code = 409
    default_detail = "user already exists."
    
class UserNotFoundError(AppException):
    status_code = 404
    default_detail = "User not found."
    
class NoneExistentError(AppException):
    status_code = 400
    default_detail = "Required information has not been entered."
    
class OTPExpiredError(AppException):
    status_code = 400
    default_detail = "otp expired."
    
class OTPWrongCode(AppException):
    status_code = 409
    default_detail = "otp code mismatch."