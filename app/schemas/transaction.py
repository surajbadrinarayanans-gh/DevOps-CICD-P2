from pydantic import BaseModel


class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    location: str
    device_id: str
