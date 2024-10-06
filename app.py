from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a random secret key for better security

# Data directories
DATA_DIR = os.path.join(os.getcwd(), "data")
ADMIN_PASTES_DIR = os.path.join(DATA_DIR, "admin")
ANON_PASTES_DIR = os.path.join(DATA_DIR, "other")

# Create directories if they don't exist
os.makedirs(ADMIN_PASTES_DIR, exist_ok=True)
os.makedirs(ANON_PASTES_DIR, exist_ok=True)

# User data storage (consider using a database in production)
users = {
    "admin": generate_password_hash("adminpassword")  # Use a secure password in production
}

@app.route("/")
def index():
    """Render the home page."""
    return render_template("home.html")

@app.route("/add_paste", methods=["GET", "POST"])
def add_paste():
    """Allow users to add an anonymous paste."""
    if request.method == "POST":
        paste_title = request.form.get("pasteTitle").replace("/", "%2F")  # Escape slashes
        paste_content = request.form.get("pasteContent")

        try:
            with open(os.path.join(ANON_PASTES_DIR, paste_title), "w", encoding="utf-8") as file:
                file.write(paste_content)
            flash("Paste added successfully!", "success")
        except Exception as e:
            flash(f"Error adding paste: {str(e)}", "danger")
        
        return redirect(url_for("index"))
    
    return render_template("add_paste.html")

@app.route("/users")
def users_page():
    """Render the users page."""
    return render_template("users.html")

@app.route("/upgrades")
def upgrades():
    """Render the upgrades page."""
    return render_template("upgrades.html")

@app.route("/hall_of_autism")
def hall_of_autism():
    """Render the hall of autism page with data from hol.json."""
    try:
        with open(os.path.join(DATA_DIR, "hol.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
        return render_template("hall_of_autism.html", loosers=data.get("loosers", []))
    except Exception as e:
        flash(f"Error loading hall of autism data: {str(e)}", "danger")
        return redirect(url_for("index"))

@app.route("/tos")
def tos():
    """Render the terms of service page."""
    return render_template("tos.html")

@app.route("/telegram")
def telegram():
    """Render the Telegram page."""
    return render_template("telegram.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash("Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid credentials. Please try again.", "danger")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Handle user logout."""
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username already exists.", "danger")
        else:
            users[username] = generate_password_hash(password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Render the admin dashboard, showing admin posts."""
    if 'username' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("login"))
    
    admin_posts = os.listdir(ADMIN_PASTES_DIR)
    return render_template("admin_dashboard.html", admin_posts=admin_posts)

@app.route("/admin/add_post", methods=["GET", "POST"])
def admin_add_post():
    """Allow admin to add a new post."""
    if 'username' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        paste_title = request.form.get("pasteTitle").replace("/", "%2F")  # Escape slashes
        paste_content = request.form.get("pasteContent")

        try:
            with open(os.path.join(ADMIN_PASTES_DIR, paste_title), "w", encoding="utf-8") as file:
                file.write(paste_content)
            flash("Admin post added successfully!", "success")
        except Exception as e:
            flash(f"Error adding admin post: {str(e)}", "danger")
        
        return redirect(url_for("admin_dashboard"))
    
    return render_template("admin_add_post.html")

@app.route("/admin/delete_post/<post_title>")
def delete_post(post_title):
    """Allow admin to delete a specific post."""
    if 'username' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    try:
        os.remove(os.path.join(ADMIN_PASTES_DIR, post_title))
        flash("Post deleted successfully!", "success")
    except FileNotFoundError:
        flash("Post not found.", "danger")
    except Exception as e:
        flash(f"Error deleting post: {str(e)}", "danger")
    
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)  # Listen on all interfaces
