from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


#database for storing user details
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts=db.relationship('Post',backref='user',passive_deletes=True)
    comments=db.relationship('Comment',backref='user',passive_deletes=True)
    
    saveds=db.relationship('Saved',backref='user',passive_deletes=True)
#database for storing posts 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading=db.Column(db.Text,nullable=False)
    formatting=db.Column(db.Text)
    text=db.Column(db.Text,nullable=False)
    tags=db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author=db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    comments=db.relationship('Comment',backref='post',passive_deletes=True)
     
    saveds=db.relationship('Saved',backref='post',passive_deletes=True)
#database for storing comments
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text,nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author=db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False)

#post for storing the saved post of an user 
class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author=db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"),nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id',ondelete="CASCADE"),nullable=False)


