from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from enum import Enum
from datetime import datetime

from db import get_db
from models import USERS, GOALS, CYCLES, QUARTERLY_UPDATES, MANAGER_CHECKINS
from schema import (
    UserRegister,
    GoalCreate,
    GoalUpdate,
    GoalApproval,
    QuarterlyUpdateCreate,
    ManagerCheckinCreate,
    CycleCreate,
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)

router = APIRouter(prefix="/api", tags=["Hackathon API"])


# ======================================================
# ENUMS
# ======================================================

class ApprovalStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"


# ======================================================
# HELPERS
# ======================================================


def success_response(message: str, data=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow(),
    }



def get_active_cycle(db: Session):
    cycle = db.query(CYCLES).filter(CYCLES.is_active == True).first()

    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active cycle found",
        )

    return cycle



def get_goal_or_404(goal_id: UUID, db: Session):
    goal = db.query(GOALS).filter(GOALS.id == goal_id).first()

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found",
        )

    return goal



def latest_progress(goal_id: UUID, db: Session):
    update = (
        db.query(QUARTERLY_UPDATES)
        .filter(QUARTERLY_UPDATES.goal_id == goal_id)
        .order_by(QUARTERLY_UPDATES.id.desc())
        .first()
    )

    if not update:
        return 0.0

    return float(update.completion_percentage or 0)



def serialize_goal(goal, db: Session):
    cycle = db.query(CYCLES).filter(CYCLES.id == goal.cycle_id).first()

    employee = db.query(USERS).filter(USERS.id == goal.employee_id).first()

    return {
        "id": str(goal.id),
        "title": goal.title,
        "description": goal.description,
        "thrust_area": goal.thrust_area,
        "uom_type": goal.uom_type,
        "target_value": goal.target_value,
        "weightage": goal.weightage,
        "approval_status": goal.approval_status,
        "locked": goal.locked,
        "is_shared": goal.is_shared,
        "employee": {
            "id": str(employee.id) if employee else None,
            "name": employee.name if employee else None,
            "email": employee.email if employee else None,
        },
        "cycle": {
            "id": str(cycle.id) if cycle else None,
            "name": cycle.name if cycle else None,
            "phase": cycle.phase if cycle else None,
        },
        "progress": latest_progress(goal.id, db),
        "created_at": goal.created_at,
    }


# ======================================================
# AUTH
# ======================================================


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(USERS).filter(USERS.email == data.email).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        user = USERS(
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
            role=data.role,
            department=data.department,
            manager_id=data.manager_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return success_response(
            "User registered successfully",
            {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
            },
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error",
        )


@router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(USERS).filter(USERS.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id), db)

    return success_response(
        "Login successful",
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        },
    )


# ======================================================
# USER
# ======================================================


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return success_response(
        "Profile fetched successfully",
        {
            "id": str(current_user.id),
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "department": current_user.department,
        },
    )


# ======================================================
# CYCLES
# ======================================================


@router.post("/cycles", status_code=status.HTTP_201_CREATED)
def create_cycle(
    data: CycleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create cycles",
        )

    try:
        if data.is_active:
            active_cycles = db.query(CYCLES).filter(CYCLES.is_active == True).all()

            for cycle in active_cycles:
                cycle.is_active = False

        cycle = CYCLES(
            name=data.name,
            phase=data.phase,
            start_date=data.start_date,
            end_date=data.end_date,
            is_active=data.is_active,
        )

        db.add(cycle)
        db.commit()
        db.refresh(cycle)

        return success_response(
            "Cycle created successfully",
            {
                "id": str(cycle.id),
                "name": cycle.name,
                "phase": cycle.phase,
                "is_active": cycle.is_active,
            },
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create cycle",
        )


@router.get("/cycles")
def get_cycles(db: Session = Depends(get_db)):
    cycles = db.query(CYCLES).order_by(CYCLES.created_at.desc()).all()

    data = []

    for cycle in cycles:
        data.append(
            {
                "id": str(cycle.id),
                "name": cycle.name,
                "phase": cycle.phase,
                "is_active": cycle.is_active,
                "start_date": cycle.start_date,
                "end_date": cycle.end_date,
            }
        )

    return success_response("Cycles fetched successfully", data)


# ======================================================
# GOALS
# ======================================================


@router.post("/goals", status_code=status.HTTP_201_CREATED)
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    active_cycle = get_active_cycle(db)

    goal_count = (
        db.query(GOALS)
        .filter(
            GOALS.employee_id == current_user.id,
            GOALS.cycle_id == active_cycle.id,
        )
        .count()
    )

    if goal_count >= 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 8 goals allowed",
        )

    existing_goals = (
        db.query(GOALS)
        .filter(
            GOALS.employee_id == current_user.id,
            GOALS.cycle_id == active_cycle.id,
        )
        .all()
    )

    total_weightage = sum(goal.weightage for goal in existing_goals)

    if total_weightage + data.weightage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total weightage exceeds 100",
        )

    try:
        goal = GOALS(
            employee_id=current_user.id,
            cycle_id=active_cycle.id,
            thrust_area=data.thrust_area,
            title=data.title,
            description=data.description,
            uom_type=data.uom_type,
            target_value=data.target_value,
            weightage=data.weightage,
            is_shared=data.is_shared,
            approval_status=ApprovalStatus.PENDING.value,
            locked=False,
        )

        db.add(goal)
        db.commit()
        db.refresh(goal)

        return success_response(
            "Goal created successfully",
            serialize_goal(goal, db),
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create goal",
        )


@router.get("/goals/my-goals")
def my_goals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    goals = (
        db.query(GOALS)
        .filter(GOALS.employee_id == current_user.id)
        .order_by(GOALS.created_at.desc())
        .all()
    )

    return success_response(
        "Goals fetched successfully",
        [serialize_goal(goal, db) for goal in goals],
    )


@router.put("/goals/{goal_id}")
def update_goal(
    goal_id: UUID,
    data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    goal = get_goal_or_404(goal_id, db)

    if goal.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access",
        )

    if goal.locked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal is locked",
        )

    updated_weightage = (
        data.weightage
        if data.weightage is not None
        else goal.weightage
    )

    other_goals = (
        db.query(GOALS)
        .filter(
            GOALS.employee_id == current_user.id,
            GOALS.id != goal.id,
        )
        .all()
    )

    total_weightage = sum(g.weightage for g in other_goals)

    if total_weightage + updated_weightage > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Weightage exceeds 100",
        )

    try:
        update_data = data.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(goal, key, value)

        goal.approval_status = ApprovalStatus.PENDING.value

        db.commit()
        db.refresh(goal)

        return success_response(
            "Goal updated successfully",
            serialize_goal(goal, db),
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update goal",
        )


# ======================================================
# MANAGER
# ======================================================


@router.get("/manager/team-goals")
def get_team_goals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can access this endpoint",
        )

    team_members = (
        db.query(USERS)
        .filter(USERS.manager_id == current_user.id)
        .all()
    )

    employee_ids = [employee.id for employee in team_members]

    goals = (
        db.query(GOALS)
        .filter(GOALS.employee_id.in_(employee_ids))
        .all()
    )

    return success_response(
        "Team goals fetched successfully",
        [serialize_goal(goal, db) for goal in goals],
    )


@router.put("/goals/{goal_id}/approval")
def approve_goal(
    goal_id: UUID,
    data: GoalApproval,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can approve goals",
        )

    goal = get_goal_or_404(goal_id, db)

    employee = db.query(USERS).filter(USERS.id == goal.employee_id).first()

    if not employee or employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee does not belong to your team",
        )

    try:
        goal.approval_status = data.approval_status
        goal.locked = data.approval_status == ApprovalStatus.APPROVED.value

        db.commit()

        return success_response(
            f"Goal {data.approval_status.lower()} successfully",
            serialize_goal(goal, db),
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Approval failed",
        )


# ======================================================
# QUARTERLY UPDATE
# ======================================================


@router.post("/goals/{goal_id}/quarterly-update")
def quarterly_update(
    goal_id: UUID,
    data: QuarterlyUpdateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    goal = get_goal_or_404(goal_id, db)

    if goal.employee_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized access",
        )

    existing_quarter = (
        db.query(QUARTERLY_UPDATES)
        .filter(
            QUARTERLY_UPDATES.goal_id == goal_id,
            QUARTERLY_UPDATES.quarter == data.quarter,
        )
        .first()
    )

    if existing_quarter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quarter already updated",
        )

    completion = 0

    if data.actual_achievement and data.planned_target:
        completion = (
            data.actual_achievement / data.planned_target
        ) * 100

    try:
        update = QUARTERLY_UPDATES(
            goal_id=goal_id,
            quarter=data.quarter,
            planned_target=data.planned_target,
            actual_achievement=data.actual_achievement,
            progress_status=data.progress_status,
            completion_percentage=completion,
            employee_comment=data.employee_comment,
        )

        db.add(update)
        db.commit()
        db.refresh(update)

        return success_response(
            "Quarterly update submitted successfully",
            {
                "id": str(update.id),
                "quarter": update.quarter,
                "completion_percentage": update.completion_percentage,
            },
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit update",
        )


# ======================================================
# MANAGER CHECKIN
# ======================================================


@router.post("/checkins/{update_id}")
def manager_checkin(
    update_id: UUID,
    data: ManagerCheckinCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only managers can add checkins",
        )

    update = (
        db.query(QUARTERLY_UPDATES)
        .filter(QUARTERLY_UPDATES.id == update_id)
        .first()
    )

    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quarterly update not found",
        )

    goal = db.query(GOALS).filter(GOALS.id == update.goal_id).first()

    employee = db.query(USERS).filter(USERS.id == goal.employee_id).first()

    if employee.manager_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized team access",
        )

    try:
        checkin = MANAGER_CHECKINS(
            update_id=update_id,
            manager_id=current_user.id,
            comment=data.comment,
        )

        db.add(checkin)
        db.commit()
        db.refresh(checkin)

        return success_response(
            "Manager checkin added successfully",
            {
                "id": str(checkin.id),
                "comment": checkin.comment,
            },
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add checkin",
        )


# ======================================================
# ADMIN
# ======================================================


@router.get("/admin/all-goals")
def get_all_goals(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint",
        )

    goals = db.query(GOALS).all()

    return success_response(
        "All goals fetched successfully",
        [serialize_goal(goal, db) for goal in goals],
    )


@router.get("/admin/users")
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access this endpoint",
        )

    users = db.query(USERS).all()

    result = []

    for user in users:
        goal_count = (
            db.query(GOALS)
            .filter(GOALS.employee_id == user.id)
            .count()
        )

        result.append(
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "department": user.department,
                "goal_count": goal_count,
            }
        )

    return success_response("Users fetched successfully", result)
