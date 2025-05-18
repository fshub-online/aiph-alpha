from sqlalchemy import String, Float, Enum, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
import enum

class KeyResultStatus(enum.Enum):
    FUTURE = "FUTURE"
    CURRENT = "CURRENT"
    PAST = "PAST"

class KeyResultComplexityLevel(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class KeyResult(Base):
    __tablename__ = "key_results"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    start_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[KeyResultStatus] = mapped_column(Enum(KeyResultStatus), nullable=False)
    complexity_level: Mapped[KeyResultComplexityLevel | None] = mapped_column(Enum(KeyResultComplexityLevel), nullable=True)
    due_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    objective_id: Mapped[int] = mapped_column(Integer, ForeignKey("objectives.id"), nullable=False)
    team_member_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("team_members.id"), nullable=True)

    objective = relationship("Objective", back_populates="key_results")
    team_member = relationship("TeamMember", back_populates="key_results")
