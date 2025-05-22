from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = db.relationship('BookSearch', backref='user', lazy='dynamic')
    saved_books = db.relationship('SavedBook', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BookSearch(db.Model):
    __tablename__ = 'book_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    search_query = db.Column(db.String(255))
    search_type = db.Column(db.String(50))
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedBook(db.Model):
    __tablename__ = 'saved_books'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    work_key = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
    author_name = db.Column(db.String(255))
    author_key = db.Column(db.String(50))
    publisher = db.Column(db.String(255))
    publication_date = db.Column(db.String(50))
    isbn = db.Column(db.String(20))
    edition_count = db.Column(db.Integer)
    cover_id = db.Column(db.Integer)
    ebook_access = db.Column(db.String(50))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'work_key'),)