from flask import (Blueprint, render_template, redirect,
   url_for, flash, session)
from flask_login import current_user, login_user, logout_user, login_required
from forms import LoginForm, MessageForm, RegisterForm
from app import db
from sqlalchemy import and_, or_
from models import User, Post, Message
from flask import Flask, render_template, request, redirect
from datetime import datetime ,date

bp = Blueprint('app', __name__,  url_prefix='')

@bp.route('/')
@login_required
def top():
   users = User.query.all()
   return render_template('talk.html', users=users)
   

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


@bp.route('/top2', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts, today=date.today())

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

@bp.route('/create')
def create():
    return render_template('create.html')

@bp.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)

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
