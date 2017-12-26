import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
import bcrypt

from django.contrib.auth.models import update_last_login, user_logged_in
user_logged_in.disconnect(update_last_login)

# Create your models here.
Base = declarative_base()
engine = sqlalchemy.create_engine('sqlite:///db.sqlite3?check_same_thread=False')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(Text)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def check_password(self, raw_password):
        # TODO: Make this auto update using
        # check_passwords setter argument
        return bcrypt.hashpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


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


# User._meta.pk.to_python = User.password



