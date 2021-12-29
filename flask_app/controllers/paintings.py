from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.artist import Artist


@app.route('/new/painting')
def new_painting():
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['artist_id']
    }
    return render_template('new_painting.html',artist=Artist.get_by_id(data))


@app.route('/create/painting',methods=['POST'])
def create_painting():
    if 'artist_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect('/new/painting')
    # if submit 'artist_id' not in session:
    #     return redirect('dashboard')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": int(request.form["price"]),
        "artist_id": session["artist_id"]
    }
    Painting.save(data)
    return redirect('/dashboard')

@app.route('/edit/painting/<int:id>')
def edit_painting(id):
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    artist_data = {
        "id":session['artist_id']
    }
    return render_template("edit_painting.html",edit=Painting.get_one(data),artist=Artist.get_by_id(artist_data))

@app.route('/update/painting',methods=['POST'])
def update_painting():
    if 'artist_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect(f"/edit/painting/{request.form['id']}")
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": int(request.form["price"]),
        "id": request.form['id']
        }
    Painting.update(data)
    return redirect('/dashboard')

@app.route('/painting/<int:id>')
def show_painting(id):
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
        }
    artist_data = {
        "id":session['artist_id']
        }
    return render_template("show_painting.html",painting=Painting.get_one(data), logged_in_user=Artist.get_by_id(artist_data))

@app.route('/destroy/painting/<int:id>')
def destroy_painting(id):
    if 'artist_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
        }
    Painting.destroy(data)
    return redirect('/dashboard')