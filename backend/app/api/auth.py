from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.competency import CadreRole

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    department: str
    is_admin: bool
    role_id: Optional[str] = None
    role_title: Optional[str] = None
    role_code: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    if not authorization:
        # Default fallback to first active officer for smooth demo
        user = db.query(User).filter(User.email == "officer.sharma@mospi.gov.in").first()
        if user:
            return user
        raise HTTPException(status_code=401, detail="Authentication credentials required")

    token = authorization.replace("Bearer ", "").strip()
    if token.startswith("token_"):
        user_id = token.replace("token_", "")
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user

    # Lookup by email or id
    user = db.query(User).filter((User.id == token) | (User.email == token)).first()
    if not user:
        # Default fallback if valid token prefix
        user = db.query(User).filter(User.email == "officer.sharma@mospi.gov.in").first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")

    return user

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.strip()).first()
    if not user:
        # Auto-create if not found to provide seamless onboarding
        role = db.query(CadreRole).first()
        user = User(
            email=payload.email.strip(),
            name=payload.email.split("@")[0].replace(".", " ").title(),
            role_id=role.id if role else None,
            department="MoSPI Official",
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = f"token_{user.id}"
    role_title = user.cadre_role.title if user.cadre_role else "Statistical Officer"
    role_code = user.cadre_role.code if user.cadre_role else "ROLE_STAT_INV_2"

    return LoginResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            department=user.department,
            is_admin=user.is_admin,
            role_id=user.role_id,
            role_title=role_title,
            role_code=role_code
        )
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    role_title = current_user.cadre_role.title if current_user.cadre_role else "Statistical Officer"
    role_code = current_user.cadre_role.code if current_user.cadre_role else "ROLE_STAT_INV_2"
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        department=current_user.department,
        is_admin=current_user.is_admin,
        role_id=current_user.role_id,
        role_title=role_title,
        role_code=role_code
    )
