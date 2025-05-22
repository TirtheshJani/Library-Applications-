from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Simple in-memory user database
users = {}

# Mock book database
# books = [
#     {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
#     {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949},
#     {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
#     {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
#     {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951}
# ]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('You were successfully logged in')
            return redirect(url_for('book_search'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            error = 'Username already exists. Please choose a different one.'
        else:
            users[username] = {'password': password}
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

@app.route('/book-search', methods=['GET', 'POST'])
def book_search():
    if not session.get('logged_in'):
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    
    search_results = []
    if request.method == 'POST':
        search_query = request.form['search_query'].lower()
        search_results = [book for book in books 
                         if search_query in book['title'].lower() 
                         or search_query in book['author'].lower()]
    
    return render_template('book_search.html', books=search_results, username=session.get('username'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)