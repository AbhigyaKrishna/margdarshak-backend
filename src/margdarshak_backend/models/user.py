from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserData(BaseModel):
    user_id: Optional[str] = None
    name: str
    date_of_birth: datetime
    time_of_birth: time
    gender: Gender
    state: str
    city: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            time: lambda v: v.isoformat()
        } 