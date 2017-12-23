import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

# Create your models here.
Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(Text)


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey(User.id))


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    blog_id = Column(Integer, ForeignKey(Blog.id))
    content = Column(String)
    author_id = Column(Integer, ForeignKey(User.id))



