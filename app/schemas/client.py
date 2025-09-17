from pydantic import BaseModel

class OTPRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp_code: str

class OTPResponse(BaseModel):
    message: str
    success: bool