from fastapi import (
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.user import User


from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_secure_password,
    oauth2_scheme,
    decode_access_token
)

from app.services.email_service import (
    send_account_email
)


def create_user(
    db: Session,
    email: str,
    username: str
):
    # Check existing user
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return {
            "success": False,
            "message": "User already exists"
        }

    # Generate secure password
    generated_password = generate_secure_password()

    # Hash generated password
    hashed_password = hash_password(
        generated_password
    )

    # Create database user
    new_user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        role="recruiter"
    )

    # Save user
    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    # Send onboarding email
    email_sent = send_account_email(
        to_email=email,
        username=username,
        password=generated_password
    )

    if not email_sent:
        return {
            "success": False,
            "message": "User created but email failed"
        }

    return {
        "success": True,
        "message": "User created successfully"
    }


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    # Find user
    user = db.query(User).filter(
        User.email == email
    ).first()

    # User not found
    if not user:
        return None

    # Verify password
    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    payload = decode_access_token(token)

    if payload is None:

        raise credentials_exception
    
    email: str = payload.get("sub")
    
    if email is None:

        raise credentials_exception
    
    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise credentials_exception
    
    return user

def require_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user

def require_roles(
        allowed_roles: list
):
    def role_checker(
            current_user: User = Depends(get_current_user)
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return current_user
    
    return role_checker