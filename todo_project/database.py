from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from constants import DatabaseConstants

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# POSTGRESQL_DATABASE_URL = 'postgresql://sagarsadhu:Postgresql$321@localhost/TodoApplicationDatabase'


DATABASE_URL = DatabaseConstants.MYSQL_DATABASE_URL

if 'sqlite' in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(
        DATABASE_URL
    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
