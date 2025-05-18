from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
import sqlite3
import bcrypt
import jwt
import pyotp
import datetime
from functools import wraps
import re
from metadata_mapping import MetadataMapper  # Import the previous mapping class

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'  # Change in production
app.config['JWT_SECRET'] = 'your-jwt-secret-change-this'  # Change in production

# Initialize database
def init_db():
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            totp_secret TEXT NOT NULL
        )''')
        conn.commit()

# Input sanitization
def sanitize_input(input_str):
    if not input_str:
        return input_str
    # Remove dangerous characters and limit length
    return re.sub(r'[^\w\s@.-]', '', input_str)[:100]

# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            jwt.decode(token, app.config['JWT_SECRET'], algorithms=['HS256'])
        except:
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    totp = StringField('2FA Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = sanitize_input(form.username.data)
        password = form.password.data
        totp_code = form.totp.data

        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                totp = pyotp.TOTP(user[3])
                if totp.verify(totp_code):
                    token = jwt.encode({
                        'user_id': user[0],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                    }, app.config['JWT_SECRET'])
                    session['token'] = token
                    return redirect(url_for('mapper'))
                else:
                    return render_template('login.html', form=form, error='Invalid 2FA code')
            else:
                return render_template('login.html', form=form, error='Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()  # Reusing form for simplicity
    if form.validate_on_submit():
        username = sanitize_input(form.username.data)
        password = form.password.data
        totp_secret = pyotp.random_base32()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            with sqlite3.connect('users.db') as conn:
                c = conn.cursor()
                c.execute('INSERT INTO users (username, password, totp_secret) VALUES (?, ?, ?)',
                         (username, hashed_password.decode('utf-8'), totp_secret))
                conn.commit()
            return render_template('register.html', form=form, totp_secret=totp_secret,
                                 message='Registration successful. Save this TOTP secret for 2FA.')
        except sqlite3.IntegrityError:
            return render_template('register.html', form=form, error='Username already exists')
    return render_template('register.html', form=form)

@app.route('/mapper', methods=['GET', 'POST'])
@token_required
def mapper():
    if request.method == 'POST':
        try:
            data = request.get_json()
            mapper = MetadataMapper()
            if data.get('direction') == 'cgcore_to_iso':
                result = mapper.cgcore_to_iso19115(data.get('metadata'))
            else:
                result = mapper.iso19115_to_cgcore(data.get('metadata'))
            return jsonify({'result': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    return render_template('mapper.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
