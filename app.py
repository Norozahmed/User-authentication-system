from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from db import execute_query
import secrets
import os
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
import os
import re

load_dotenv()  

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') 

# Configuration
app.config['SECRET_KEY'] = 'your-very-secure-secret-key-123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config.update(
    SESSION_COOKIE_SECURE=True,    # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax'  # CSRF protection
)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper Functions
def allowed_file(filename):
    return ('.' in filename and 
            filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS'])

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Add this function near the top of your file
def is_password_strong(password):
    """
    Validate password strength
    Returns (bool, str): (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    return True, ""

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = execute_query(
            "SELECT id, username, password FROM users WHERE email = %s",
            (email,),
            fetch_one=True
        )
        
        if user and check_password_hash(user['password'], password):
            # Store user info in session
            session.clear()  # Clear session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True   # Set permanent
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        profile_pic = request.files.get('profile_pic')

        # Basic validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))

        # Check if username exists
        existing_user = execute_query(
            "SELECT id FROM users WHERE username = %s",
            (username,),
            fetch_one=True
        )
        if existing_user:
            flash('Username already exists', 'error')
            return redirect(url_for('register'))

        # Check if email exists
        existing_email = execute_query(
            "SELECT id FROM users WHERE email = %s",
            (email,),
            fetch_one=True
        )
        if existing_email:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Handle profile picture upload
        profile_pic_path = None
        if profile_pic and profile_pic.filename:
            if allowed_file(profile_pic.filename):
                filename = secure_filename(profile_pic.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                profile_pic_path = os.path.join('static/uploads', filename)
                try:
                    os.makedirs('static/uploads', exist_ok=True)
                    profile_pic.save(profile_pic_path)
                except Exception as e:
                    print(f"Error saving profile picture: {e}")
                    flash('Error uploading profile picture', 'error')
                    return redirect(url_for('register'))
            else:
                flash('Invalid file type for profile picture', 'error')
                return redirect(url_for('register'))

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        try:
            user_id = execute_query(
                """
                INSERT INTO users (username, email, password, profile_pic, created_at)
                VALUES (%s, %s, %s, %s, NOW())
                """,
                (username, email, hashed_password, profile_pic_path)
            )
            
            if user_id:
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                if profile_pic_path and os.path.exists(profile_pic_path):
                    os.remove(profile_pic_path)
                flash('Registration failed. Please try again.', 'error')
                print("Database insert returned None")
                return redirect(url_for('register'))
                
        except Exception as e:
            print(f"Registration error: {e}")
            if profile_pic_path and os.path.exists(profile_pic_path):
                os.remove(profile_pic_path)
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        user = execute_query(
            "SELECT id, username FROM users WHERE email = %s",
            (email,),
            fetch_one=True
        )
        
        if user:
            # Generate reset token (valid for 1 hour)
            reset_token = secrets.token_urlsafe(32)
            expiry_time = datetime.now() + timedelta(hours=1)
            
            # Store token in database
            execute_query(
                "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE id = %s",
                (reset_token, expiry_time, user['id'])
            )
            
            flash('Password reset link has been sent to your email', 'info')
            return redirect(url_for('login'))
        else:
            flash('Email not found in our system', 'danger')
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verify token is valid and not expired
    user = execute_query(
        "SELECT id, reset_token_expiry FROM users WHERE reset_token = %s",
        (token,),
        fetch_one=True
    )
    
    if not user or datetime.now() > user['reset_token_expiry']:
        flash('Invalid or expired reset link', 'danger')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        new_password = generate_password_hash(request.form['password'])
        
        # Update password and clear reset token
        execute_query(
            "UPDATE users SET password = %s, reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
            (new_password, user['id'])
        )
        
        flash('Password updated successfully! Please login', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

@app.route('/dashboard')
@login_required
def dashboard():
    user = execute_query(
        """SELECT username, email, profile_pic 
        FROM users WHERE id = %s""",
        (session['user_id'],),
        fetch_one=True
    )
    
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    user = execute_query(
        """SELECT username, email, full_name, bio, skills, profile_pic 
        FROM users WHERE id = %s""",
        (session['user_id'],),
        fetch_one=True
    )
    
    return render_template('profile.html', user=user)

@app.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        bio = request.form.get('bio')
        skills = request.form.get('skills')
        
        # Get current username from database
        current_user = execute_query(
            "SELECT username FROM users WHERE id = %s",
            (session['user_id'],),
            fetch_one=True
        )
        
        # Handle file upload
        profile_pic = None
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user['username']}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                profile_pic = filename
        
        # Update database
        if profile_pic:
            execute_query(
                """UPDATE users 
                SET full_name = %s, bio = %s, skills = %s, profile_pic = %s 
                WHERE id = %s""",
                (full_name, bio, skills, profile_pic, session['user_id'])
            )
        else:
            execute_query(
                """UPDATE users 
                SET full_name = %s, bio = %s, skills = %s 
                WHERE id = %s""",
                (full_name, bio, skills, session['user_id'])
            )
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # GET request - show current profile data
    user = execute_query(
        "SELECT full_name, bio, skills FROM users WHERE id = %s",
        (session['user_id'],),
        fetch_one=True
    )
    
    return render_template('update_profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)