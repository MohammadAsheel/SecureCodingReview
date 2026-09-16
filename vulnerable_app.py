from flask import Flask, request, render_template_string
import sqlite3
import os
import platform

app = Flask(__name__)

# Hardcoded Secret (Vulnerability 1: Sensitive Data Exposure)
SECRET_API_KEY = "12345-abcde-super-secret-key"

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute('''INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')''')
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
        <title>Vulnerable App Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
            .banner { background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }
            .container-main { max-width: 600px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; border-bottom: 1px solid #edf2f7; padding: 15px 20px; }
            .card-body { padding: 20px; }
        </style>
    </head>
    <body>
        <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Vulnerable Dashboard</div>
                <div class="card-body">
                    <p class="mb-4">Welcome to the vulnerable app! Select a module to test:</p>
                    <div class="d-grid gap-2">
                        <a href="/login" class="btn btn-outline-danger">Login (SQLi)</a>
                        <a href="/greet" class="btn btn-outline-danger">Greet (XSS)</a>
                        <a href="/ping" class="btn btn-outline-danger">Ping (Command Injection)</a>
                        <a href="/admin" class="btn btn-outline-danger">Admin (Broken Access Control)</a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

# SQL Injection (Vulnerability 2)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        # Vulnerable SQL query using string formatting
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Login Success</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
                    .banner {{ background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }}
                    .container-main {{ max-width: 600px; margin: 40px auto; }}
                    .card {{ border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                    .card-header {{ background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }}
                </style>
            </head>
            <body>
                <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
                <div class="container container-main">
                    <div class="card">
                        <div class="card-header">Login Success</div>
                        <div class="card-body text-center p-4">
                            <h4 class="text-success mb-3">Welcome, {username}!</h4>
                            <p class="text-muted">You have successfully authenticated.</p>
                            <a href="/" class="btn btn-secondary mt-3">Back to Dashboard</a>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''
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
                    .banner { background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }
                    .container-main { max-width: 600px; margin: 40px auto; }
                    .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
                    .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
                </style>
            </head>
            <body>
                <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
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
            .banner { background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }
            .container-main { max-width: 500px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
        </style>
    </head>
    <body>
        <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
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
                        <button type="submit" class="btn btn-danger w-100 mb-2">Sign In</button>
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

# Cross-Site Scripting - XSS (Vulnerability 3)
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # Vulnerable to Reflected XSS
    template = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Greet</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
            .banner {{ background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }}
            .container-main {{ max-width: 600px; margin: 40px auto; }}
            .card {{ border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .card-header {{ background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }}
        </style>
    </head>
    <body>
        <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Greeting Service</div>
                <div class="card-body text-center p-4">
                    <h3 class="mb-4">Hello, {name}!</h3>
                    <p class="text-muted small mb-4">Try adding ?name=&lt;script&gt;alert(1)&lt;/script&gt; to the URL.</p>
                    <a href="/" class="btn btn-secondary">Back to Dashboard</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)

# Command Injection (Vulnerability 4)
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '127.0.0.1')
    # Vulnerable to Command Injection
    count_flag = "-n" if platform.system() == "Windows" else "-c"
    response = os.popen(f"ping {count_flag} 1 {ip}").read()
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Ping Utility</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
            .banner {{ background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }}
            .container-main {{ max-width: 700px; margin: 40px auto; }}
            .card {{ border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .card-header {{ background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }}
        </style>
    </head>
    <body>
        <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
        <div class="container container-main">
            <div class="card">
                <div class="card-header">Network Ping Tool</div>
                <div class="card-body p-4">
                    <p class="text-muted small mb-3">Ping results for IP: {ip}</p>
                    <div class="bg-light p-3 rounded border mb-4">
                        <pre class="mb-0" style="white-space: pre-wrap;">{response}</pre>
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

# Missing Authentication (Vulnerability 5)
@app.route('/admin')
def admin():
    # Anyone can access this page without logging in!
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Admin Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
            .banner { background-color: #800000; color: #ffffff; padding: 15px; text-align: center; font-weight: 500; border-bottom: 1px solid #500000; }
            .container-main { max-width: 600px; margin: 40px auto; }
            .card { border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
            .card-header { background-color: #fff; font-weight: 600; border-top-left-radius: 10px !important; border-top-right-radius: 10px !important; padding: 15px 20px; }
        </style>
    </head>
    <body>
        <div class="banner">⚠️ This application intentionally contains security vulnerabilities for educational purposes.</div>
        <div class="container container-main">
            <div class="card border-danger">
                <div class="card-header bg-danger text-white">Admin Dashboard</div>
                <div class="card-body p-4">
                    <h5 class="text-danger mb-3">Warning: Unauthenticated Access Detected</h5>
                    <p class="mb-4">Welcome to the secret admin area. You have full control because access control is broken.</p>
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
