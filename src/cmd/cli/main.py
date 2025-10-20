import click,uuid
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.application.ports.password_hasher_repository import PasswordHasher
from src.core.database import create_db_engine,Base
from src.modules.user.infrastructure.persistence.models import Users
from src.modules.movie.infrastructure.persistence.models import Movies
from src.modules.reserve.infrastructure.persistence.models import Reservations
from src.config.settings import AppSettings
from sqlalchemy.orm import sessionmaker
from src.modules.auth.exceptions import DuplicateUserException
from src.modules.user.entity.user import User, UserRole
from datetime import datetime



@click.group()
def cli(): ...


@click.command
def create_super_user():
    engine= create_db_engine(AppSettings().database)
    db_session  = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    
    user_repo:UserRepository = PostgresUserRepository(db_session)
    password_hasher:PasswordHasher = BcryptPasswordHasher()
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

@click.command
def init_database_tables():
    engine= create_db_engine(AppSettings().database)
    Base.metadata.create_all(bind=engine)
    click.echo("Database created")




cli.add_command(create_super_user)
cli.add_command(init_database_tables)


if __name__ == '__main__':
    cli()