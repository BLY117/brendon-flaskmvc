from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from App.models import Competition, CompetitonUser, User, db

from.index import index_views

from App.controllers import (
    create_user,
    authenticate, 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

@auth_view.route('/', methods=['GET'])
def get_home_page():
    competitions = Competition.query.all()
    return render_template("home.html", competitions=competitions)

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/login', methods=['GET'])
def get_login_page():
    users = get_all_users()
    return render_template('login.html', users=users)

@auth_views.route('/logout', methods=['GET'])
def logout_action():
  #logout_user()
  flash('Logged Out')
  return redirect(url_for('auth_views.get_login_page'))

@auth_views.route('/signup', methods=['GET'])
def get_signup_page():
    users = get_all_users()
    return render_template('signup.html', users=users)

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@auth_views.route('/login', methods=['POST'])
def user_login_api():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        flash('Logged in successfully.')
        #login_user(user)
        return redirect(url_for('auth_views.get_home_page'))
    else:
        return jsonify(message='bad username or password given'), 401
    return redirect('/login')

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})