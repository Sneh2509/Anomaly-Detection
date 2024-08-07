from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.route('/')
def home():
    user = session.get('user')  # Retrieve the logged-in user's info from session
    return render_template('home.html', user=user)

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']
        user = User.query.filter((User.email == email_or_username) | (User.username == email_or_username)).first()
        if user and check_password_hash(user.password, password):
            session['user'] = {'username': user.username, 'email': user.email}
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match!', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
