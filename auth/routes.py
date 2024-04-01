import flask
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from auth import bp
from auth.forms import LoginForm, RegisterForm
from models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)

        if user is None and User.check_password(form.password.data):
            return flask.redirect(flask.url_for('auth.login'))
        login_user(user)
        return flask.redirect(flask.url_for('main.all_recipes'))

    return render_template('login_page.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        User.add_user(flask.request.form['username'])

        flash('Congratulations you have successfully registered a user!')
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out')
    return redirect(url_for('main.index'))
