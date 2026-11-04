from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JournalIn(BaseModel):
    symbol: str = Field(min_length=2, max_length=32)
    side: str = Field(pattern="^(BUY|SELL)$")
    entry_price: float = Field(gt=0)
    exit_price: float | None = Field(default=None, gt=0)
    quantity: float = Field(ge=0)
    notes: str = Field(default="", max_length=4000)

class PositionIn(BaseModel):
    symbol: str = Field(min_length=2, max_length=32)
    quantity: float = Field(gt=0)
    average_price: float = Field(gt=0)
    market: str = Field(default="CRYPTO", pattern="^(CRYPTO|NSE|BSE|US)$")
