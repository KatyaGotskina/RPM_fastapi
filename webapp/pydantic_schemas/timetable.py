from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TimetableCreateModel(BaseModel):
    doctor_id: int
    user_id: int
    service_id: int
    start: datetime