from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.expression import text, null
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_on = Column(TIMESTAMP(timezone=True),server_default=text('Now()'), nullable=False)
