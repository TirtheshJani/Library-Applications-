from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import requests
from config import Config
from models import db, User, BookSearch, SavedBook
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# OpenLibrary API Helper Functions
class OpenLibraryAPI:
    @staticmethod
    def search_books(query, search_type='q', limit=20):

        #Search for books using OpenLibrary API
        #search_type can be: 'q' (general), 'title', 'author'
        url = f"{Config.OPENLIBRARY_BASE_URL}/search.json"
        
        params = {
            search_type: query,
            'limit': limit,
            'fields': 'key,title,author_name,author_key,first_publish_year,publisher,publication_date,isbn,cover_i,edition_count,ebook_access'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    @staticmethod
    def get_cover_url(cover_id, size='M'):
        """Get book cover URL. Size can be 'S', 'M', or 'L'"""
        if cover_id:
            return f"{Config.OPENLIBRARY_COVERS_URL}/b/id/{cover_id}-{size}.jpg"
        return None
    
    @staticmethod
    def get_editions(work_key, limit=10):
        """Get editions for a specific work"""
        url = f"{Config.OPENLIBRARY_BASE_URL}/search.json"
        params = {
            'q': f'key:{work_key}',
            'fields': 'key,title,publisher,publish_date,isbn',
            'limit': limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None

# Test database connection
def test_db_connection():
    try:
        with app.app_context():
            # Try to execute a simple query
            db.session.execute('SELECT 1')
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Routes
@app.route('/')
def index():
    return render_template('base.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('search'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')
<<<<<<< Updated upstream

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('search'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')
=======
# OAuth Routes
@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('search'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)

@app.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('search'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}', 'error')
        return redirect(url_for('login'))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args.get('state') != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})
    
    if response.status_code != 200:
        abort(401)
    
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    
    if response.status_code != 200:
        abort(401)
    
    email = provider_data['userinfo']['email'](response.json())

    # find or create the user in the database
    user = User.query.filter_by(email=email).first()
    if user is None:
        # Create new user from OAuth
        username = email.split('@')[0]  # Use email prefix as username
        
        # Make sure username is unique
        counter = 1
        original_username = username
        while User.query.filter_by(username=username).first():
            username = f"{original_username}_{counter}"
            counter += 1
        
        user = User(email=email, username=username)
        # For OAuth users, we don't set a password
        user.password_hash = ''  # Empty password hash for OAuth users
        db.session.add(user)
        db.session.commit()
        
        flash(f'Welcome! Your account has been created via {provider.title()}.', 'success')
    else:
        flash(f'Welcome back! Logged in via {provider.title()}.', 'success')

    # log the user in
    login_user(user)
    return redirect(url_for('search'))
>>>>>>> Stashed changes

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/api/search', methods=['POST'])
@login_required
def api_search():
    """API endpoint for book search"""
    data = request.get_json()
    query = data.get('query')
    search_type = data.get('search_type', 'q')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # Log the search
    search_log = BookSearch(
        user_id=current_user.id,
        search_query=query,
        search_type=search_type
    )
    db.session.add(search_log)
    db.session.commit()
    
    # Search using OpenLibrary API
    results = OpenLibraryAPI.search_books(query, search_type)
    
    if not results:
        return jsonify({'error': 'Failed to fetch results'}), 500
    
    # Process results
    books = []
    for doc in results.get('docs', []):
        book = {
            'key': doc.get('key'),
            'title': doc.get('title'),
            'author_name': ', '.join(doc.get('author_name', [])) if doc.get('author_name') else 'Unknown',
            'author_key': doc.get('author_key', [None])[0] if doc.get('author_key') else None,
            'publisher': ', '.join(doc.get('publisher', [])[:3]) if doc.get('publisher') else 'Unknown',
            'first_publish_year': doc.get('first_publish_year', 'Unknown'),
            'isbn': doc.get('isbn', [None])[0] if doc.get('isbn') else None,
            'edition_count': doc.get('edition_count', 0),
            'ebook_access': doc.get('ebook_access', 'no_ebook'),
            'cover_url': OpenLibraryAPI.get_cover_url(doc.get('cover_i'))
        }
        books.append(book)
    
    return jsonify({
        'success': True,
        'count': results.get('numFound', 0),
        'books': books
    })

@app.route('/api/save-book', methods=['POST'])
@login_required
def save_book():
    """Save a book to user's collection"""
    data = request.get_json()
    
    # Check if book already saved
    existing = SavedBook.query.filter_by(
        user_id=current_user.id,
        work_key=data.get('work_key')
    ).first()
    
    if existing:
        return jsonify({'error': 'Book already saved'}), 400
    
    saved_book = SavedBook(
        user_id=current_user.id,
        work_key=data.get('work_key'),
        title=data.get('title'),
        author_name=data.get('author_name'),
        author_key=data.get('author_key'),
        publisher=data.get('publisher'),
        publication_date=str(data.get('first_publish_year', '')),
        isbn=data.get('isbn'),
        edition_count=data.get('edition_count', 0),
        cover_id=data.get('cover_id'),
        ebook_access=data.get('ebook_access')
    )
    
    db.session.add(saved_book)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Book saved successfully'})

@app.route('/saved-books')
@login_required
def saved_books():
    """Display user's saved books"""
    books = current_user.saved_books.all()
    return render_template('saved_books.html', books=books)

# Database initialization
@app.route('/init-db')
def init_db():
    """Initialize database tables - useful for setup"""
    try:
        db.create_all()
        return "Database tables created successfully!"
    except Exception as e:
        return f"Error creating tables: {e}"

if __name__ == '__main__':
    with app.app_context():
        # Test the database connection first
        if test_db_connection():
            # Create tables if connection is successful
            try:
                db.create_all()
                print("📚 Database tables created successfully!")
            except Exception as e:
                print(f"❌ Error creating tables: {e}")
        else:
            print("🔧 Please check your database configuration and network settings.")
    
    app.run(debug=True)