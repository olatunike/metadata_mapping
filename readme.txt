pip install flask flask-wtf bcrypt pyotp pyjwt

    Save all files in the appropriate structure (templates in a templates folder).
    Run app.py to start the Flask server.
    Access the application at http://localhost:5000.
    Register a new user, save the TOTP secret, and use an authenticator app (e.g., Google Authenticator) for 2FA.
    Log in with username, password, and 2FA code to access the metadata mapper.

Security features implemented:

    Password Hashing: Uses bcrypt for secure password storage.
    2FA: Implements TOTP-based 2FA with pyotp.
    Injection Prevention: Sanitizes inputs and uses parameterized SQLite queries.
    Session Management: Uses JWT tokens with expiration.
    CSRF Protection: Flask-WTF provides CSRF tokens for forms.
    Input Validation: WTForms validates input lengths and requirements.

Note: Change the secret keys in app.py for production use, and consider using a more robust database (e.g., PostgreSQL) for scalability.
