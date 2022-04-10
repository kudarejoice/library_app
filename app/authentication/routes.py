from forms import UserLoginForm
from models import User, db
from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    form = UserLoginForm()


    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)

        user = User(email, password = password)

        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully created a user account {email}', 'User-created')
        return redirect(url_for('site.home'))
    # raise Exception('Invalid form data: Please check your form')
    return render_template('sign_up.html', form = form)

@auth.route('/sign_in', methods = ['Get', 'Post'])
def sign_in():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You have successfully logged into your account!', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Unfortunately, the details you have entered are incorrect. Please try again.', 'auth-failed')
                return redirect(url_for('auth.sign_in'))
    except:
        raise Exception('Invalid form data. Please try again.')
    return render_template('sign_in.html', form=form)
