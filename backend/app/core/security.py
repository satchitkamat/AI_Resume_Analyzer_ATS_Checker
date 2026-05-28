import os
import secrets
import string

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv


load_dotenv()


# =========================
# ENVIRONMENT VARIABLES
# =========================

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)


# =========================
# PASSWORD HASHING
# =========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =========================
# OAUTH2 CONFIGURATION
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================
# PASSWORD HASHING FUNCTION
# =========================

def hash_password(password: str) -> str:

    # bcrypt safe limit
    password = password[:72]

    return pwd_context.hash(password)


# =========================
# PASSWORD VERIFICATION
# =========================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    plain_password = plain_password[:72]

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================
# ACCESS TOKEN CREATION
# =========================

def create_access_token(
    data: dict
) -> str:

    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================
# ACCESS TOKEN DECODING
# =========================

def decode_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# =========================
# RANDOM PASSWORD GENERATOR
# =========================

def generate_secure_password(
    length: int = 12
) -> str:

    MAX_LENGTH = 32

    length = min(length, MAX_LENGTH)

    characters = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*"
    )

    password = ''.join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return password