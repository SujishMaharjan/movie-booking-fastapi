import click,uuid
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.user.infrastructure import user_postgres_repository
from src.modules.user.entity.user import User, UserRole
from datetime import datetime
from src.modules.auth.exceptions import DuplicateUserException



def create_super_user(user_repo:UserRepository,password_hasher:PasswordHasher):
    click.echo("Creating Super")
    try:
        name = click.prompt("Full Name")

        # Prompt + validate phone
        phone = click.prompt("Phone")
        if user_repo.get_by_phone(phone):
            click.secho(" Phone already exists. Aborting.", fg="red")
            raise DuplicateUserException("Phone already exists")
        
        
        # Prompt + validate email
        email = click.prompt("Email")
        if user_repo.get_by_email(email):
            click.secho("Email already exists. Aborting.", fg="red")
            raise DuplicateUserException("Email already exists")
        
        username = click.prompt("Username")
        if user_repo.get_by_username(username):
            click.secho("Username already exists. Aborting.", fg="red")
            raise DuplicateUserException("Username already exists")

        password = click.prompt("Password", hide_input=True, confirmation_prompt=True)
        hashed_password = password_hasher.hash_password(password)
        role = UserRole.ADMIN
        created_at = datetime.now()
        id = str(uuid.uuid4())

        user = User(id,name,phone,email,username,hashed_password,created_at,role)
        user = user_repo.to_persistence_model(user)
        user_repo.save(user)
        click.secho(f"Super user with username {username} created")

    except Exception as e:
        click.secho(f"Error: {e}", fg="red")


