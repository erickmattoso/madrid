from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Float, Text, String, DateTime
from sqlalchemy import Column

Base = declarative_base()

class User(Base):
    """User account."""
    
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    bio = Column(Text)
    avatar_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"

class Places(Base):
    """Places are locations"""

    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    country = Column(String(255),nullable=False)
    state = Column(String(255))
    city = Column(String(255),nullable=False)
    placename = Column(String(255),nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Places {self.placesname}>"

class Routes(Base):
    """routes are filters """

    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    routename = Column(String(255), unique=True, nullable=False)
    usersid = Column(Integer)
    placesid = Column(Integer)
    def __repr__(self):
        return f"<Routes {self.routesname}>"

class Comments(Base):
    """comments are filters """

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    comment_text = Column(Text)
    routestatus = Column(Integer)
    usersid = Column(Integer)
    placesid = Column(Integer)

    def __repr__(self):
        return f"<Comments {self.comment_text}>"

class Testing(Base):
    """testing are filters """

    __tablename__ = "travelOptimization.testing"

    # id = Column(Integer, primary_key=True, autoincrement="auto")
    ADDRESS_ID = Column(String(255), primary_key=True)
    INDIVIDUAL_ID = Column(String(255))
    FIRST_NAME = Column(String(255))
    LAST_NAME = Column(String(255))


    def __repr__(self):
        return f"<testing {self.INDIVIDUAL_ID}>"