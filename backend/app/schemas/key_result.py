from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel
from app.models.key_result import KeyResultStatus, KeyResultComplexityLevel


class KeyResultBase(BaseModel):
    description: str
    target_value: float
    current_value: float
    start_value: Optional[float] = None
    unit: str
    status: KeyResultStatus
    complexity_level: Optional[KeyResultComplexityLevel] = None
    due_date: Optional[date] = None
    objective_id: int
    team_member_id: Optional[int] = None


class KeyResultCreate(KeyResultBase):
    pass


class KeyResultUpdate(BaseModel):
    description: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    start_value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[KeyResultStatus] = None
    complexity_level: Optional[KeyResultComplexityLevel] = None
    due_date: Optional[date] = None
    objective_id: Optional[int] = None
    team_member_id: Optional[int] = None


class KeyResultInDBBase(KeyResultBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KeyResult(KeyResultInDBBase):
    pass


class KeyResultInDB(KeyResultInDBBase):
    pass
