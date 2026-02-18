"""
User
id
name
lastname
email 
password
username
birthday
city
reg_date


UserPost
id
uid
text
reg_date

PostPhoto
id
photo_path
pid
reg_date


Comment
id
text
uid
pid
reg_date

"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lastname = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    birthday = Column(String)
    city = Column(String)
    reg_date = Column(DateTime, default=datetime.now())


class UserPost(Base):
    __tablename__ = "userposts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey("users.id"))
    text = Column(String, nullable=False)
    reg_date  = Column(DateTime, default=datetime.now())

    user_fk = relationship("User", lazy="subquery")


class PostPhoto(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_path = Column(String, nullable=False)
    pid = Column(Integer, ForeignKey("userposts.id"))
    reg_date = Column(DateTime, default=datetime.now())
    
    post_fk = relationship("UserPost", lazy="subquery")



class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    uid = Column(Integer, ForeignKey("users.id"))
    pid = Column(Integer, ForeignKey("userposts.id"))
    reg_date = Column(DateTime, default=datetime.now())
    
    user_fk = relationship("User", lazy="subquery")
    post_fk = relationship("UserPost", lazy="subquery")




