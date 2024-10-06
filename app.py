from flask import Flask, render_template, request, url_for, redirect, session, flash
import os
import json
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a random secret key in production

# Data folder paths
DATA = os.path.join(os.getcwd(), "data")
ADMIN_PASTES = os.path.join(DATA, "admin")
ANON_PASTES = os.path.join(DATA, "other")

# Load template
with open(os.path.join(DATA, "template"), "r", encoding="utf-8") as temp_file:
    _DEFAULT_POST_TEMPLATE = temp_file.read()

# Sample admin credentials (replace this with a database or config file in production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("password")  # Change this to a hashed password

admin_posts_list = []
anon_posts_list = []
loosers_list = []

# Other functions remain unchanged...

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if credentials are valid
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('admin_logged_in', None)  # Remove admin from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route("/new_admin_post", methods=['POST'])
def new_admin_post_form_post():
    if not session.get('admin_logged_in'):
        flash('You must be logged in to create admin posts.', 'danger')
        return redirect(url_for('login'))

    global _DEFAULT_POST_TEMPLATE
    try:
        args = request.values
        pasteTitle = str(args.get('pasteTitle')).replace("/", "%2F")
        pasteContent = args.get('pasteContent')

        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}_{pasteTitle}"
    except Exception as e:
        return f"Error: {e}"

    with open(os.path.join(ADMIN_PASTES, filename), "w", encoding="utf-8") as file:
        file.write(pasteContent)
    return redirect(url_for('index'))

# Protect the admin post route
@app.route("/admin/<file>")
def admin_post(file):
    if not session.get('admin_logged_in'):
        flash('You must be logged in to view this page.', 'danger')
        return redirect(url_for('login'))

    filename = os.path.join(ADMIN_PASTES, file)
    with open(filename, "r", encoding="utf-8") as filec:
        content = filec.read()
    stats = os.stat(filename)
    creation_date = datetime.utcfromtimestamp(int(stats.st_mtime)).strftime('%d-%m-%Y')
    creation_time = datetime.utcfromtimestamp(int(stats.st_mtime)).strftime('%H:%M:%S')
    size = bytes2KB(stats.st_size)
    return render_template(
        "admin.html",
        filename=file,
        file_content=content,
        creation_date=creation_date,
        creation_time=creation_time,
        size=size
    )

# ... (rest of the routes remain unchanged)

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080, debug=False)
