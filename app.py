"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = '38432084'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

@app.route('/')
def redirect_users():
    """Redirects to list of all users in db"""
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Shows form to add a new user"""
    return render_template('new_user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Inserts new user to db, and redirect to user detail page"""
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    image_url = request.form["imageURL"]
    last_name = last_name if last_name else None
    image_url = image_url if image_url else None
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Shows user detail page"""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    """Shows edit page for specific user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Shows edit page for specific user"""
    u = User.query.get_or_404(user_id)
    u.first_name = request.form["firstName"] if request.form["firstName"] else u.first_name
    u.last_name = request.form["lastName"] if request.form["lastName"] else u.last_name
    u.image_url = request.form["imageURL"] if request.form["imageURL"] else u.image_url
    db.session.add(u)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user from db"""
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/users')