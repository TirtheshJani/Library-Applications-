from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
    
    def __repr__(self):
        return f'<User {self.username}>'

class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    search_query = db.Column(db.String(200), nullable=False)
    search_type = db.Column(db.String(50), nullable=False)  # 'title', 'author', 'general'
    results_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime)
    
    def __init__(self, user_id, search_query, search_type, results_count=0):
        self.user_id = user_id
        self.search_query = search_query
        self.search_type = search_type
        self.results_count = results_count
    
    def __repr__(self):
        return f'<SearchHistory {self.search_query}>'

class OpenLibraryBook:
    """Model to represent a book from Open Library API"""
    
    def __init__(self, api_data):
        self.key = api_data.get('key', '')
        self.title = api_data.get('title', 'Unknown Title')
        self.authors = api_data.get('author_name', [])
        self.author_keys = api_data.get('author_key', [])
        self.first_publish_year = api_data.get('first_publish_year')
        self.edition_count = api_data.get('edition_count', 0)
        self.cover_id = api_data.get('cover_i')
        self.languages = api_data.get('language', [])
        self.isbn = api_data.get('isbn', [])
        self.publishers = api_data.get('publisher', [])
        self.publish_dates = api_data.get('publish_date', [])
        self.subjects = api_data.get('subject', [])
        self.ebook_access = api_data.get('ebook_access', 'no_ebook')
        self.lending_edition = api_data.get('lending_edition_s')
        self.has_fulltext = api_data.get('has_fulltext', False)
    
    @property
    def primary_author(self):
        """Get the first author or 'Unknown Author'"""
        return self.authors[0] if self.authors else 'Unknown Author'
    
    @property
    def authors_string(self):
        """Get authors as a comma-separated string"""
        return ', '.join(self.authors) if self.authors else 'Unknown Author'
    
    @property
    def cover_url(self):
        """Get cover image URL"""
        if self.cover_id:
            return f"https://covers.openlibrary.org/b/id/{self.cover_id}-M.jpg"
        return None
    
    @property
    def openlibrary_url(self):
        """Get Open Library URL for this book"""
        return f"https://openlibrary.org{self.key}" if self.key else None
    
    @property
    def primary_isbn(self):
        """Get the first ISBN if available"""
        return self.isbn[0] if self.isbn else None
    
    @property
    def publication_info(self):
        """Get formatted publication information"""
        info_parts = []
        
        if self.first_publish_year:
            info_parts.append(f"First published: {self.first_publish_year}")
        
        if self.edition_count:
            info_parts.append(f"{self.edition_count} edition(s)")
        
        if self.publishers:
            info_parts.append(f"Publisher: {self.publishers[0]}")
        
        return " | ".join(info_parts) if info_parts else "Publication info not available"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'key': self.key,
            'title': self.title,
            'authors': self.authors,
            'primary_author': self.primary_author,
            'first_publish_year': self.first_publish_year,
            'edition_count': self.edition_count,
            'cover_url': self.cover_url,
            'openlibrary_url': self.openlibrary_url,
            'isbn': self.primary_isbn,
            'publication_info': self.publication_info,
            'languages': self.languages,
            'ebook_access': self.ebook_access,
            'has_fulltext': self.has_fulltext
        }


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)