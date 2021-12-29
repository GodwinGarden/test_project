from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.artist import Artist
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not Artist.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        }
    id = Artist.save(data)
    session['artist_id'] = id

    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    artist = Artist.get_by_email(request.form)

    if not artist:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(artist.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['artist_id'] = artist.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'artist_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['artist_id']
        }
    return render_template("dashboard.html",artist=Artist.get_by_id(data),paintings=Painting.get_all_with_artists())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')