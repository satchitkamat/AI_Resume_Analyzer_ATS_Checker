from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.auth import (
    CreateUserRequest,
    UserLogin
)

from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_current_user,
    require_admin
)

from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

from fastapi.security import OAuth2PasswordRequestForm


# =====================================
# CREATE USER API
# =====================================

@router.post("/create-user/admin-only")

def create_new_user(
    user_data: CreateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    result = create_user(
        db=db,
        email=user_data.email,
        username=user_data.username
    )
    if not result["success"]:
    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=["Message"]
        )
        
    return result

# =====================================
# LOGIN API
# =====================================

@router.post("/login")

def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if not result:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return result


@router.get("/me")

def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@router.get("/admin-only")

def admin_only_route(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "user": current_user.email
    }