from sqlalchemy import Column, String, Float, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class KeyResultStatus(str, enum.Enum):
    FUTURE = "FUTURE"
    CURRENT = "CURRENT"
    PAST = "PAST"

class ComplexityLevel(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class KeyResult(Base):
    __tablename__ = "key_results"

    description = Column(String, nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    start_value = Column(Float, nullable=True)
    unit = Column(String, nullable=False)
    status = Column(Enum(KeyResultStatus), nullable=False)
    complexity_level = Column(Enum(ComplexityLevel), nullable=True)
    due_date = Column(Date, nullable=True)
    objective_id = Column(String, ForeignKey("objectives.id"), nullable=False)
    team_member_id = Column(String, ForeignKey("team_members.id"), nullable=True)

    objective = relationship("Objective", back_populates="key_results")
    team_member = relationship("TeamMember", back_populates="key_results")
