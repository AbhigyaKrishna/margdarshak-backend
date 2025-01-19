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
    
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Convert time object to string in HH:MM:SS format
        if "time_of_birth" in data and isinstance(data["time_of_birth"], time):
            data["time_of_birth"] = data["time_of_birth"].strftime("%H:%M:%S")
        # Convert datetime objects to ISO format strings
        if "date_of_birth" in data and isinstance(data["date_of_birth"], datetime):
            data["date_of_birth"] = data["date_of_birth"].isoformat()
        if "created_at" in data and isinstance(data["created_at"], datetime):
            data["created_at"] = data["created_at"].isoformat()
        return data
    
    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        # Convert string back to time object if needed
        if isinstance(obj.get("time_of_birth"), str):
            try:
                hour, minute, second = map(int, obj["time_of_birth"].split(":"))
                obj["time_of_birth"] = time(hour, minute, second)
            except (ValueError, TypeError):
                pass
        # Convert ISO strings back to datetime if needed
        if isinstance(obj.get("date_of_birth"), str):
            try:
                obj["date_of_birth"] = datetime.fromisoformat(obj["date_of_birth"])
            except (ValueError, TypeError):
                pass
        if isinstance(obj.get("created_at"), str):
            try:
                obj["created_at"] = datetime.fromisoformat(obj["created_at"])
            except (ValueError, TypeError):
                pass
        return super().model_validate(obj, *args, **kwargs) 