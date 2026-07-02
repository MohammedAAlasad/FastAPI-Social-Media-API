from collections.abc import AsyncGenerator
import uuid 

from fastapi import Depends
from sqlalchemy import Column, String , Text , DateTime , ForeignKey ,UUID
from sqlalchemy.ext.asyncio import async_session, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase , relationship
from datetime import datetime 
from fastapi_users.db import SQLAlchemyUserDatabase  ,SQLAlchemyBaseUserTableUUID


DATABSE_URL = "sqlite+aiosqlite:///./test.db"

class base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID , base): 
    __tablename__ = "user"
    posts = relationship(argument="Post" , back_populates="user")



class Post(base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid = True) , primary_key=True , default=uuid.uuid4)  # columns struct
    user_id = Column(UUID(as_uuid = True) , ForeignKey("user.id") , nullable= False)
    caption = Column(Text)
    url = Column(String , nullable=False)
    file_type = Column(String , nullable=False)
    file_name = Column(String , nullable=False)
    created_at = Column(DateTime , default=datetime.utcnow)

    user = relationship(argument="User" , back_populates="posts") #  in User class search for posts 

engine = create_async_engine(DATABSE_URL)
async_session_maker = async_sessionmaker(engine , expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession , None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db( session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session , User)