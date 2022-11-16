from flask import (Blueprint, render_template, redirect,
   url_for, flash, session)
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, MessageForm, NewpostForm, RegisterForm
from app import db
from sqlalchemy import and_, or_, desc
from models import User, Post, Message
from flask import Flask, render_template, request, redirect
from datetime import datetime ,date
import json

bp = Blueprint('app', __name__,  url_prefix='')
   

@bp.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user:
           if user.password == form.password.data:
               login_user(user)
               return redirect(url_for('app.top'))
           else:
               flash('Invalid password.')
               return redirect(url_for('app.login'))
       else:
           flash('The email address is not registered.')
           return redirect(url_for('app.login'))
   return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('app.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
       user = User(
           username=form.username.data,
           email=form.email.data,
           password=form.username.data
       )
       db.session.add(user)
       db.session.commit()
       flash('Your info is registered correctly!')
       return redirect(url_for('app.login'))
   return render_template('register.html', form=form)

@bp.route('/', methods=['GET'])
def get():
    dict= ""
    room_type = {}
    posts = Post.query.all()
    return render_template('index.html', posts=posts, dict=dict, room_type=room_type)

@bp.route('/', methods=['POST'])
def post():
    filters = []
    dropdown_value = request.form.get('dropdown_value')
    min_rent = request.form.get('min_rent')
    max_rent = request.form.get('max_rent')
    is_bill_included = request.form.get('is_bill_included')
    start_date = request.form.get('start_date')
    room_type = request.form.getlist('room_type')
    duration = request.form.get('duration')
    is_furnished = request.form.get('is_furnished')
    gender = request.form.get('gender')
    is_smorkable = request.form.get('is_smorkable')
    with_landload = request.form.get('with_landload')

    if min_rent != '':
        min_rent = int(min_rent)
        filters.append(Post.monthly_rent >= min_rent)
    if max_rent != '':
        max_rent = int(request.form.get('max_rent'))
        filters.append(Post.monthly_rent <= max_rent)
    if ((is_bill_included is not None) and (is_bill_included == 'true')):
        filters.append(Post.is_bill_included == 'TRUE')
    if start_date == 'current_date':
        filters.append(Post.start_date <= datetime.today())
    elif start_date == 'specified_date':
        specified_date = request.form.get('specified_date')
        filters.append(Post.start_date >= specified_date)
    if len(room_type):
        filters.append(Post.room_type.in_(room_type))
    if duration:
        filters.append(Post.duration <= duration)
    if is_furnished:
        filters.append(Post.is_furnished == is_furnished)
    if gender:
        if gender == "female":
            filters.append(Post.gender == "female")
        elif gender =="male":
            filters.append(Post.gender == "male")
    if is_smorkable:
        filters.append(Post.is_smorkable == is_smorkable)
    if with_landload:
        filters.append(Post.with_landload == with_landload)
    
    if dropdown_value:
        if dropdown_value == 'created_at':
            posts = Post.query.filter(and_(*filters)).order_by(desc(dropdown_value))
        elif dropdown_value == 'monthly_rent':
            posts = Post.query.filter(and_(*filters)).order_by(dropdown_value)
    else:
        posts = Post.query.filter(and_(*filters))

    dict = request.form
    for key in dict:
        print ("form key " + key + " " +dict[key] )
    
    return render_template('index.html', posts=posts, dict=dict, room_type=room_type)


@bp.route('/create',methods=['GET'])
def create_get():
    form = NewpostForm()
    return render_template('create.html', form=form)

@bp.route('/create',methods=['POST'])
def create():   
    form = NewpostForm()
    # if request.method =="GET":
        # return render_template('create.html', form=form)
    if form.validate_on_submit():
       post = Post(
        title = request.form.get('title'),
        detail = request.form.get('detail'),
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
       )
       db.session.add(post)
       db.session.commit()
       flash('投稿が追加されました')
       return redirect(url_for('app.post'))
    # return redirect('/')
    return render_template('create.html', form=form)

@bp.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    with open('mapping.json') as f:
        jsn = json.load(f)
    print(jsn)
    print( post.is_bill_included)
    post.room_type = jsn[post.room_type]
    post.is_bill_included = jsn['is_bill_included'][str(post.is_bill_included)]
    post.is_furnished = jsn['is_furnished'][str(post.is_furnished)]
    post.gender = jsn['gender'][post.gender]
    post.is_smorkable = jsn['is_smorkable'][str(post.is_smorkable)]

    return render_template('detail.html', post=post)

@bp.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

@bp.route('/chat', methods=['GET', 'POST'])
@bp.route('/chat/<int:to_>', methods=['GET', 'POST'])
@login_required
@login_required
def chat(to_=None):
    form = MessageForm()
    if to_:
        session['to_'] = to_
    if form.validate_on_submit():
        message = Message(
            body=form.message.data,
            from_=current_user.id,
            to_=session['to_']
            )
        db.session.add(message)
        db.session.commit()
    messages = Message.query.filter(
        or_(
            and_(
                Message.from_ == session['to_'],
                Message.to_ == current_user.id
            ),
            and_(
                Message.from_ == current_user.id,
                Message.to_ == session['to_']
            ),
        )
    )
    return render_template('chat.html', form=form, messages=messages)
