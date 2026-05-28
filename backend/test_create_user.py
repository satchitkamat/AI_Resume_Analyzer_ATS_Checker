from app.core.database import SessionLocal

from app.services.auth_service import create_user


db = SessionLocal()

result = create_user(
    db=db,
    email="satchitkamat22@gmail.com",
    username="Satchit"
)

print(result)