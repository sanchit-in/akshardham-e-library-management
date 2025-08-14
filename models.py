from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(100), nullable=False)
   
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.passhash, password)

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"))
    file = db.Column(db.String)
    image = db.Column(db.String)
    feedback = db.Column(db.String)
    feedback_writer = db.Column(db.Integer, db.ForeignKey('user.id'))

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String)
    books = db.relationship('Book', backref='section', lazy=True)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    passhash = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    books_issued = db.relationship('Book', secondary='books_issued', backref='User', lazy=True)
    registration_date = db.Column(db.DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passhash, password)

books_issued = db.Table('books_issued',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class Request_book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    book_status = db.Column(db.String(20), nullable=False, default='pending')
    return_date = db.Column(db.DateTime, nullable=True)

    reader = db.relationship('User', backref='requests')
    book = db.relationship('Book', backref='requests')

class Feedback(db.Model):
    
    id=db.Column(db.Integer, primary_key=True)
    book_id=db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback=db.Column(db.Text, nullable=False)

    book=db.relationship('Book',backref=db.backref('feedbacks' , lazy=True ))
    user=db.relationship('User',backref=db.backref('feedbacks',lazy=True))
