import click
from src.entrypoints.cli import user
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher
from src.core.infrastucture.persistence.database_postgres import create_db_engine,get_db_session
from src.config.settings import DatabaseSettings,AppSettings
from sqlalchemy.orm import sessionmaker

@click.group()
def cli(): ...


@click.command
def create_super_user():
    engine= create_db_engine(AppSettings().database)
    db_session  = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    
    user_repo = PostgresUserRepository(db_session)
    password_hasher = BcryptPasswordHasher()
    user.create_super_user(user_repo,password_hasher)

@click.command
def init_db():
    click.echo("Database created")

cli.add_command(create_super_user)
cli.add_command(init_db)

if __name__ == '__main__':
    cli()