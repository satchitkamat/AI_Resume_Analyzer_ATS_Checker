from app.services.email_service import send_account_email


result = send_account_email(
    to_email="satchitkamat22@gmail.com",
    username="Satchit",
    password="TempPass123@"
)

print(result)