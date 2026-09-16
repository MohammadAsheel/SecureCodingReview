from flask import Flask, request, render_template_string, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import sqlite3
import os
import subprocess
import re
import platform

app = Flask(__name__)

# FIX 1: Secrets should be loaded from environment variables, never hardcoded.
# Example: export SECRET_KEY="your-production-secret-key"
app.secret_key = os.environ.get("SECRET_KEY", "default-dev-key")

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS users''') # Drop to ensure fresh schema with hashed passwords
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    # FIX 5: Hash passwords using PBKDF2 (Werkzeug default)
    hashed_pw = generate_password_hash('admin123')
    cursor.execute('''INSERT INTO users (id, username, password) VALUES (1, 'admin', ?)''', (hashed_pw,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Secure App Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
            .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
            .container-main { max-width: 600px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; border-bottom: 1px solid #edf2f7; padding: 15px 20px; }
            .card-body { padding: 20px; }
        </style>
    </head>
    <body>
        <div class="banner">✅ This application demonstrates secure coding practices.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Secure Dashboard</div>
                <div class="card-body">
                    <p class="mb-4">Welcome to the secure app! Select a module to test:</p>
                    <div class="d-grid gap-2">
                        <a href="/login" class="btn btn-outline-success">Login (Secure)</a>
                        <a href="/greet" class="btn btn-outline-success">Greet (Secure)</a>
                        <a href="/ping" class="btn btn-outline-success">Ping (Secure)</a>
                        <a href="/admin" class="btn btn-outline-success">Admin (Secure)</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

# FIX 2 & FIX 5: Prevent SQL Injection using parameterized queries & verify hashed password
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Secure SQL query using parameterized query (?) - fetch by username
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        # Verify the hash securely using check_password_hash
        if user and check_password_hash(user[2], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Login Failed</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
                    .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
                    .container-main { max-width: 600px; margin: 40px auto; }
                    .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                    .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
                </style>
            </head>
            <body>
                <div class="banner">✅ This application demonstrates secure coding practices.</div>
                <div class="container container-main">
                    <div class="card">
                        <div class="card-header">Login Failed</div>
                        <div class="card-body text-center p-4">
                            <h4 class="text-danger mb-3">Invalid credentials.</h4>
                            <a href="/login" class="btn btn-secondary mt-3">Try Again</a>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''
            
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
            .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
            .container-main { max-width: 500px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
        </style>
    </head>
    <body>
        <div class="banner">✅ This application demonstrates secure coding practices.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Account Login</div>
                <div class="card-body p-4">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label text-muted">Username</label>
                            <input type="text" class="form-control" name="username" required>
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted">Password</label>
                            <input type="password" class="form-control" name="password" required>
                        </div>
                        <button type="submit" class="btn btn-success w-100 mb-2">Sign In</button>
                        <div class="text-center">
                            <a href="/" class="text-decoration-none text-muted small">Return to Dashboard</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

# FIX 3: Prevent XSS using templating engine variables (Jinja2 auto-escaping)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # Secure against XSS: Using Jinja2 context variables ensures auto-escaping
    template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Greet</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
            .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
            .container-main { max-width: 600px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
        </style>
    </head>
    <body>
        <div class="banner">✅ This application demonstrates secure coding practices.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Greeting Service</div>
                <div class="card-body text-center p-4">
                    <h3 class="mb-4">Hello, {{ name }}!</h3>
                    <p class="text-muted small mb-4">Try adding ?name=&lt;script&gt;alert(1)&lt;/script&gt; to the URL. It will be safely escaped.</p>
                    <a href="/" class="btn btn-secondary">Back to Dashboard</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, name=name)

# FIX 4: Prevent Command Injection by using subprocess with argument lists and input validation
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    
    # Input validation: Ensure the input looks like an IP address
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Ping Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
                .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
                .container-main { max-width: 600px; margin: 40px auto; }
                .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                .card-header { background-color: black; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
            </style>
        </head>
        <body>
            <div class="banner">✅ This application demonstrates secure coding practices.</div>
            <div class="container container-main">
                <div class="card">
                    <div class="card-header">Network Ping Tool</div>
                    <div class="card-body text-center p-4">
                        <h4 class="text-danger mb-3">Invalid IP address format.</h4>
                        <a href="/" class="btn btn-secondary mt-3">Back to Dashboard</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', 400

    try:
        # Secure: Using subprocess.run with a list of arguments avoids shell=True risks
        count_flag = "-n" if platform.system() == "Windows" else "-c"
        result = subprocess.run(['ping', count_flag, '1', ip], capture_output=True, text=True, timeout=5)
        response_text = escape(result.stdout)
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Ping Utility</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
                .banner {{ background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }}
                .container-main {{ max-width: 700px; margin: 40px auto; }}
                .card {{ border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                .card-header {{ background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }}
            </style>
        </head>
        <body>
            <div class="banner">✅ This application demonstrates secure coding practices.</div>
            <div class="container container-main">
                <div class="card">
                    <div class="card-header">Network Ping Tool</div>
                    <div class="card-body p-4">
                        <p class="text-muted small mb-3">Ping results for IP: {ip}</p>
                        <div class="bg-light p-3 rounded border mb-4">
                            <pre class="mb-0" style="white-space: pre-wrap;">{response_text}</pre>
                        </div>
                        <div class="text-center">
                            <a href="/" class="btn btn-secondary">Back to Dashboard</a>
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''
    except Exception as e:
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Ping Error</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
                .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
                .container-main { max-width: 600px; margin: 40px auto; }
                .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
            </style>
        </head>
        <body>
            <div class="banner">✅ This application demonstrates secure coding practices.</div>
            <div class="container container-main">
                <div class="card">
                    <div class="card-header">Network Ping Tool</div>
                    <div class="card-body text-center p-4">
                        <h4 class="text-danger mb-3">An error occurred during ping.</h4>
                        <a href="/" class="btn btn-secondary mt-3">Back to Dashboard</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''

# FIX 6: Prevent Missing Authentication by requiring a valid session
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Unauthorized</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
                .banner { background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }
                .container-main { max-width: 600px; margin: 40px auto; }
                .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
            </style>
        </head>
        <body>
            <div class="banner">✅ This application demonstrates secure coding practices.</div>
            <div class="container container-main">
                <div class="card">
                    <div class="card-header">Admin Access</div>
                    <div class="card-body text-center p-4">
                        <h4 class="text-danger mb-3">Unauthorized. Please login first.</h4>
                        <a href="/login" class="btn btn-secondary mt-3">Go to Login</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        ''', 401
    
    username = escape(session.get('username'))
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Admin Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
            .banner {{ background-color: #cff4fc; color: #055160; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #b6effb; }}
            .container-main {{ max-width: 600px; margin: 40px auto; }}
            .card {{ border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .card-header {{ background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }}
        </style>
    </head>
    <body>
        <div class="banner">✅ This application demonstrates secure coding practices.</div>
        <div class="container container-main">
            <div class="card border-success">
                <div class="card-header bg-success text-white">Admin Dashboard</div>
                <div class="card-body p-4">
                    <h5 class="text-success mb-3">Authentication Successful</h5>
                    <p class="mb-4">Welcome to the secure admin area, <strong>{username}</strong>.</p>
                    <a href="/" class="btn btn-outline-secondary">Back to Dashboard</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
