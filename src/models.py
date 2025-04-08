from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique= True)
    firstname: Mapped[str] = mapped_column(String(120))
    lastname: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    #relations
    posts: Mapped[list['Post']] = relationship('Post', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')

    followers: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_from_id', backref='followed')
    followings: Mapped[list['Follower']] = relationship('Follower', foreign_keys='Follower.user_to_id', backref='follower')

    #serialize
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    #relations
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment',back_populates='post')
    medias = relationship('Media', back_populates='post')


class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(120),nullable= False)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    #relationship
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255),nullable=False)
    type: Mapped[str] = mapped_column(String(120))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    #relations
    post = relationship('Post', back_populates='medias')
    
class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'),nullable= False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'),nullable= False)
     
"""
    #relations
    followers = relationship('User', foreign_keys=[user_from_id], backref = 'followers')
    followeings = relationship('User', foreign_keys=[user_to_id], backref = 'followeings')
"""