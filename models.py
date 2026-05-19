from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from datetime import datetime, timezone
from db import Base, engine

import uuid


def utcnow():
    return datetime.now(timezone.utc)


# =========================
# USERS
# =========================

class USERS(Base):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    department = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    goals = relationship(
        "GOALS",
        back_populates="employee",
        cascade="all, delete"
    )

    shared_goals_owned = relationship(
        "SHARED_GOALS",
        foreign_keys="SHARED_GOALS.primary_owner_id",
        back_populates="primary_owner",
        cascade="all, delete"
    )

    shared_goals_received = relationship(
        "SHARED_GOALS",
        foreign_keys="SHARED_GOALS.shared_employee_id",
        back_populates="shared_employee",
        cascade="all, delete"
    )

    audit_logs = relationship(
        "AUDIT_LOGS",
        back_populates="user",
        cascade="all, delete"
    )

    checkins = relationship(
        "MANAGER_CHECKINS",
        back_populates="manager",
        cascade="all, delete"
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete"
    )


# =========================
# CYCLES
# =========================

class CYCLES(Base):

    __tablename__ = "cycles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    phase = Column(String, nullable=False)

    start_date = Column(DateTime(timezone=True), nullable=False)

    end_date = Column(DateTime(timezone=True), nullable=False)

    is_active = Column(Boolean, default=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    goals = relationship(
        "GOALS",
        back_populates="cycle",
        cascade="all, delete"
    )


# =========================
# GOALS
# =========================

class GOALS(Base):

    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    cycle_id = Column(
        UUID(as_uuid=True),
        ForeignKey("cycles.id", ondelete="CASCADE"),
        nullable=False
    )

    thrust_area = Column(String, nullable=False)

    title = Column(String, nullable=False)

    description = Column(Text)

    uom_type = Column(String, nullable=False)

    target_value = Column(Float, nullable=False)

    weightage = Column(Float, nullable=False)

    status = Column(String, default="Draft")

    approval_status = Column(String, default="Pending")

    is_shared = Column(Boolean, default=False)

    locked = Column(Boolean, default=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    employee = relationship(
        "USERS",
        back_populates="goals"
    )

    cycle = relationship(
        "CYCLES",
        back_populates="goals"
    )

    shared_goals = relationship(
        "SHARED_GOALS",
        back_populates="goal",
        cascade="all, delete"
    )

    quarterly_updates = relationship(
        "QUARTERLY_UPDATES",
        back_populates="goal",
        cascade="all, delete"
    )


# =========================
# SHARED GOALS
# =========================

class SHARED_GOALS(Base):

    __tablename__ = "shared_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    goal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("goals.id", ondelete="CASCADE"),
        nullable=False
    )

    primary_owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    shared_employee_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    synced_achievement = Column(Float)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    goal = relationship(
        "GOALS",
        back_populates="shared_goals"
    )

    primary_owner = relationship(
        "USERS",
        foreign_keys=[primary_owner_id],
        back_populates="shared_goals_owned"
    )

    shared_employee = relationship(
        "USERS",
        foreign_keys=[shared_employee_id],
        back_populates="shared_goals_received"
    )


# =========================
# QUARTERLY UPDATES
# =========================

class QUARTERLY_UPDATES(Base):

    __tablename__ = "quarterly_updates"

    __table_args__ = (
        UniqueConstraint(
            "goal_id",
            "quarter",
            name="uq_goal_quarter"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    goal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("goals.id", ondelete="CASCADE"),
        nullable=False
    )

    quarter = Column(String, nullable=False)

    planned_target = Column(Float)

    actual_achievement = Column(Float)

    progress_status = Column(
        String,
        default="Not Started"
    )

    completion_percentage = Column(Float)

    employee_comment = Column(Text)

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    goal = relationship(
        "GOALS",
        back_populates="quarterly_updates"
    )

    checkins = relationship(
        "MANAGER_CHECKINS",
        back_populates="quarterly_update",
        cascade="all, delete"
    )


# =========================
# MANAGER CHECKINS
# =========================

class MANAGER_CHECKINS(Base):

    __tablename__ = "manager_checkins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    update_id = Column(
        UUID(as_uuid=True),
        ForeignKey("quarterly_updates.id", ondelete="CASCADE"),
        nullable=False
    )

    manager_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    comment = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    quarterly_update = relationship(
        "QUARTERLY_UPDATES",
        back_populates="checkins"
    )

    manager = relationship(
        "USERS",
        back_populates="checkins"
    )


# =========================
# AUDIT LOGS
# =========================

class AUDIT_LOGS(Base):

    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    table_name = Column(String, nullable=False)

    record_id = Column(UUID(as_uuid=True), nullable=False)

    action = Column(String, nullable=False)

    old_value = Column(JSONB)

    new_value = Column(JSONB)

    timestamp = Column(
        TIMESTAMP(timezone=True),
        default=utcnow
    )

    user = relationship(
        "USERS",
        back_populates="audit_logs"
    )


# =========================
# REFRESH TOKENS
# =========================

class RefreshToken(Base):

    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    token_hash = Column(String, nullable=False)

    expire = Column(
        DateTime(timezone=True),
        nullable=False
    )

    user = relationship(
        "USERS",
        back_populates="refresh_tokens"
    )


