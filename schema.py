from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import date, datetime
from uuid import UUID


# =========================================
# AUTH
# =========================================

class UserRegister(BaseModel):

    name: str = Field(..., min_length=2, max_length=100)

    email: EmailStr

    password: str = Field(..., min_length=6)

    role: Literal[
        "employee",
        "manager",
        "admin"
    ]

    department: str = Field(..., min_length=2)

    manager_id: Optional[UUID] = None


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str = "bearer"


# =========================================
# USER RESPONSE
# =========================================

class UserResponse(BaseModel):

    id: UUID

    name: str

    email: EmailStr

    role: str

    department: str

    manager_id: Optional[UUID]

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================================
# CYCLES
# =========================================

class CycleCreate(BaseModel):

    name: str

    phase: Literal[
        "Goal Setting",
        "Q1",
        "Q2",
        "Q3",
        "Q4",
        "Annual"
    ]

    start_date: date

    end_date: date

    is_active: bool = False


class CycleResponse(BaseModel):

    id: UUID

    name: str

    phase: str

    start_date: date

    end_date: date

    is_active: bool

    model_config = {
        "from_attributes": True
    }


# =========================================
# GOALS
# =========================================

class GoalCreate(BaseModel):


    thrust_area: str = Field(..., min_length=2)

    title: str = Field(..., min_length=2)

    description: Optional[str] = None

    uom_type: Literal[
        "Numeric",
        "%",
        "Timeline",
        "Zero-based"
    ]

    target_value: float = Field(..., gt=0)

    weightage: float = Field(
        ...,
        ge=10,
        le=100
    )

    is_shared: bool = False


class GoalUpdate(BaseModel):

    thrust_area: Optional[str] = None

    title: Optional[str] = None

    description: Optional[str] = None

    target_value: Optional[float] = Field(None, gt=0)

    weightage: Optional[float] = Field(
        None,
        ge=10,
        le=100
    )

    status: Optional[
        Literal[
            "Draft",
            "Submitted"
        ]
    ] = None


class GoalApproval(BaseModel):

    approval_status: Literal[
        "Approved",
        "Rejected",
        "Rework"
    ]

    manager_comment: Optional[str] = None


class GoalUnlock(BaseModel):

    unlocked: bool


class GoalResponse(BaseModel):

    id: UUID

    employee_id: UUID

    cycle_id: UUID

    thrust_area: str

    title: str

    description: Optional[str]

    uom_type: str

    target_value: float

    weightage: float

    status: str

    approval_status: str

    is_shared: bool

    locked: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================================
# SHARED GOALS
# =========================================

class SharedGoalCreate(BaseModel):

    goal_id: UUID

    shared_employee_id: UUID


class SharedGoalResponse(BaseModel):

    id: UUID

    goal_id: UUID

    primary_owner_id: UUID

    shared_employee_id: UUID

    synced_achievement: Optional[float]

    model_config = {
        "from_attributes": True
    }


# =========================================
# QUARTERLY UPDATES
# =========================================

class QuarterlyUpdateCreate(BaseModel):

    quarter: Literal[
        "Q1",
        "Q2",
        "Q3",
        "Q4"
    ]

    planned_target: Optional[float] = None

    actual_achievement: Optional[float] = None

    progress_status: Literal[
        "Not Started",
        "On Track",
        "Completed"
    ] = "Not Started"

    employee_comment: Optional[str] = None


class QuarterlyUpdateResponse(BaseModel):

    id: UUID

    goal_id: UUID

    quarter: str

    planned_target: Optional[float]

    actual_achievement: Optional[float]

    progress_status: str

    completion_percentage: Optional[float]

    employee_comment: Optional[str]

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================================
# MANAGER CHECKINS
# =========================================

class ManagerCheckinCreate(BaseModel):

    comment: str = Field(..., min_length=2)


class ManagerCheckinResponse(BaseModel):

    id: UUID

    update_id: UUID

    manager_id: UUID

    comment: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# =========================================
# AUDIT LOGS
# =========================================

class AuditLogResponse(BaseModel):

    id: UUID

    user_id: Optional[UUID]

    table_name: str

    record_id: UUID

    action: str

    old_value: Optional[dict]

    new_value: Optional[dict]

    timestamp: datetime

    model_config = {
        "from_attributes": True
    }