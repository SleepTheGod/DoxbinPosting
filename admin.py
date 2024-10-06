from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add_paste', methods=['GET', 'POST'])
def add_paste():
    if request.method == 'POST':
        # Logic to save the paste goes here
        return redirect(url_for('index'))
    return render_template('add_paste.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic to authenticate user goes here
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Logic to register user goes here
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Logic to display admin dashboard goes here
    return render_template('admin_dashboard.html', admin_posts=["Post 1", "Post 2"])

@app.route('/hall_of_autism')
def hall_of_autism():
    # Logic to display hall of autism goes here
    return render_template('hall_of_autism.html', loosers=["Loser 1", "Loser 2"])

@app.route('/tos')
def tos():
    return render_template('tos.html')

@app.route('/users')
def users():
    # Logic to display users goes here
    return render_template('users.html', users=["User 1", "User 2"])

@app.route('/telegram')
def telegram():
    return render_template('telegram.html')

if __name__ == '__main__':
    app.run(debug=True)
