import uuid
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.user.entity.user import User
from datetime import datetime
from src.modules.user.infrastructure.persistence.models import Users
from src.modules.auth.exceptions import DuplicateUserException

class RegisterUser:
    def __init__(
        self, user_repository: UserRepository, hasher_repository: PasswordHasher
    ):
        self.user_repository = user_repository
        self.hasher_repository = hasher_repository

    def execute(self, name, username, password, phone, email, role):
        self.check_duplicate_user(username, email, phone)
        hash_password = self.hasher_repository.hash_password(password)
        user = User(
            id=str(uuid.uuid4()),
            name=name,
            phone=phone,
            email=email,
            username=username,
            hashed_password=hash_password,
            created_at=datetime.now(),
            role=role,
        )
        user_data = Users(**user.__dict__)
        self.user_repository.save(user_data)
        return user

    def check_duplicate_user(self, username: str, email: str, phone: str) -> bool:

        if self.user_repository.get_by_username(username):
            raise DuplicateUserException("Username already Exist")

        if self.user_repository.get_by_email(email):
            raise DuplicateUserException("Email already Exist")

        if self.user_repository.get_by_phone(phone):
            raise DuplicateUserException("Phone already Exist")

        return True
