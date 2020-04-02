import os
import secrets
from flask import render_template, jsonify, flash, redirect, url_for, request
from blog import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.database_structure import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
  {
    'author':'Namskov',
    'title': 'UG is named Best school in Africa!',
    'content': 'Lorem ipsum dolor sit amet consecteteur adipiscing...',
    'datePosted': '31st December, 2018'
  },
  {
    'author':'Connor',
    'title': 'El Paso',
    'content': 'Lorem ipsum dolor sit amet consecteteur adipiscing...',
    'datePosted': '1st January, 2018'
  },
  {
    'author':'Jane Doe',
    'title': 'Pizza',
    'content': '',
    'datePosted': '2nd January, 2018'
  }

]



@app.route('/user', methods=['GET']) 
def get_all_users():
  users = User.query.all()
  output = []

  for user in users:
    user_data = {}
    user_data['id'] = user.id
    user_data['image_file'] = user.image_file
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    output.append(user_data)

  return jsonify({'users' : output})

@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', posts=posts)

@app.route('/about')
def about():
  return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
       return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password.data, method='sha256')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash('Account created successfully!', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
       return redirect(url_for('home'))
  form = LoginForm()
  auth = request.form
  if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
           flash(" Oops... Invalid email or password! :( ", 'danger')
      #  if user:
      #       login_user(user, remember=form.remember.data)
      #       return redirect(url_for('home'))
      #   else:
      #        flash("Oops... Invalid email or password! :(", 'danger')
  return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))


def save_picture(form_picture):
     random_hex = secrets.token_hex(8)
     _, f_ext = os.path.splitext(form_picture.filename)
     picture_fn = random_hex + f_ext
     picture_path = os.path.join(app.root_path, 'static/profiles', picture_fn)
     form_picture.save(picture_path)

     return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():

       if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

       current_user.username = form.username.data
       current_user.email = form.email.data
       db.session.commit()
       flash('Your account has been updated!', 'success')
       return redirect(url_for('account'))
  elif request.method == 'GET':
       form.username.data = current_user.username
       form.email.data = current_user.email
  image_file = url_for('static', filename=current_user.image_file) #current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)