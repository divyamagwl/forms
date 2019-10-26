from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

@app.route('/')
def index():
    return redirect(url_for('login'))

global username
@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    global username
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        login = user.query.filter_by(username=username, password=password).first()
        if login is None:
            error = 'Invalid Credentials. Please Try again.'
        else:
            return redirect(url_for('home'))
                
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        register = user(username = username, password = password)
        
        if not username :
            error = 'Username is required'
        elif not password :
            error = 'Password is required'
        else:
            if user.query.filter_by(username=username).first():
                error = 'Username already taken'
            else:
                db.session.add(register)
                db.session.commit()
                return redirect(url_for("login"))

    return render_template("register.html", error = error) 

@app.route('/home')
def home():
    global username
    return 'Hello {}'.format(username)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)