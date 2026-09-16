# CodeAlpha - Secure Coding Review

This repository contains a comprehensive **Secure Coding Review** demonstration developed for the **CodeAlpha Cybersecurity Internship**. It showcases a comparative analysis between an intentionally vulnerable web application and its hardened, secure counterpart.

---

## 📁 Project Structure

```text
CodeAlpha_SecureCoding Review/
├── vulnerable_app.py     # Flask application with intentional vulnerabilities
├── secure_app.py         # Remediated application implementing secure coding practices
├── bandit_report.txt     # Static Application Security Testing (SAST) report
├── requirements.txt      # Python dependencies
├── Screenshots/          # Demonstrations of vulnerabilities and remediations
└── README.md             # Project documentation and review findings
```

---

## 📸 Screenshots

The `Screenshots/` directory contains visual demonstrations of the vulnerable application, its secure counterpart, and the Bandit security report:

- [Vulnerable application home page](Screenshots/home_vulnerable.png)
- [Secure application home page](Screenshots/home_secure.png)
- [SQL injection demonstration](Screenshots/sql_injection.png)
- [Parameterized SQL query fix](Screenshots/sql_fixed.png)
- [Cross-site scripting demonstration](Screenshots/xss_demo.png)
- [OS command injection demonstration](Screenshots/ping_demo.png)
- [Protected admin page](Screenshots/admin_protected.png)
- [Bandit report](Screenshots/bandit_report.png)

---

## 🔍 Vulnerability Analysis & Remediations

| # | Vulnerability Category | CWE | Vulnerable Implementation (`vulnerable_app.py`) | Remediated Implementation (`secure_app.py`) | Bandit Issue |
|---|------------------------|-----|---------------------------------------------------|---------------------------------------------|--------------|
| 1 | **Sensitive Data Exposure** | CWE-259 | Hardcoded secret key (`SECRET_API_KEY`) | Loaded from environment variables (`os.environ.get("SECRET_KEY")`) | B105 (Low) |
| 2 | **SQL Injection (SQLi)** | CWE-89 | Raw f-string query formatting: `f"SELECT ... WHERE username = '{username}'"` | Parameterized SQL query (`?` placeholders) and PBKDF2 password hashing | B608 (Medium) |
| 3 | **Reflected Cross-Site Scripting (XSS)** | CWE-79 | Unsanitized input interpolated into HTML string via f-string | Jinja2 templating variables with contextual auto-escaping: `{{ name }}` | - |
| 4 | **OS Command Injection** | CWE-78 | `os.popen(f"ping -c 1 {ip}")` with shell execution | Strict regex input validation (`^\d{1,3}(\.\d{1,3}){3}$`) + argument list in `subprocess.run` (no shell) | B605 (High) |
| 5 | **Broken Access Control** | CWE-306 | `/admin` endpoint accessible without session verification | Route guarded by checking `session.get('logged_in')` | - |
| 6 | **Debug Mode Enabled** | CWE-94 | `app.run(debug=True)` exposing debugger PIN and interactive shell | Configurable environment-based debug toggle | B201 (High) |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Vulnerable Application
```bash
python vulnerable_app.py
```
Visit `http://127.0.0.1:5000` in your web browser.

### 4. Run the Secure Application
```bash
python secure_app.py
```
Visit `http://127.0.0.1:5000` in your web browser.

---

## 🛡️ Running SAST (Static Analysis) with Bandit

To perform automated static code analysis:

```bash
# Scan vulnerable code
bandit -r vulnerable_app.py -o bandit_report.txt -f txt

# Scan secure code
bandit -r secure_app.py
```
