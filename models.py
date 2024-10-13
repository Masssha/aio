import datetime
import os
import atexit

from sqlalchemy import create_engine, String, DateTime, Integer, func, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'LLllMMmmqwerty654321')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'posts')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5439')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(PG_DSN)

atexit.register(engine.dispose)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Post(Base):
    __tablename__ = 'user_posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    owner_id: Mapped['User'] = mapped_column(ForeignKey('users.id'))
    owner_name: Mapped['User'] = mapped_column(ForeignKey('users.name'))
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.title,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner_name': self.owner_name,
            'registration_time': self.registration_time.isoformat()
        }


Base.metadata.create_all(bind=engine)