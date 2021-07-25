from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from . import auth
from .. import db
from ..email import send_email
from ..models import User
from .forms import ChangeEmailForm, ChangePasswordForm, LoginForm, PasswordResetForm, PasswordResetRequestForm, \
    RegistrationForm


@auth.before_app_request
def before_app_request():
    """
    Will intercept requests to all endpoints except static files and pages in the auth namespace
    if the user if logged in and their account is unconfirmed
    :return: if intercepted redirect to unconfirmed page
    """
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('login', methods=['GET', 'POST'])
def login():
    """
    If no form sent then GET request so return login page
    Else attempt to log user in
    :return: login page if GET or wrong password, else return to the sending page or index
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # If prompted to login from page get that page from request information
            next_page = request.args.get('next')
            # Override any maliciously passed next_page parameters
            if next_page is None or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are now logged out.")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_account_confirmation_token()
        send_email(new_user.email, 'Confirm your Hedgehog Account', '/auth/email/confirmation', user=new_user,
                   token=token)
        flash('A confirmation email has been sent to complete the registration process')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirmation/<token>')
@login_required
def confirmation(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Account created successfully.')
    else:
        flash('The confirmation link has expired or is invalid')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Password change successfully.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/confirmation')
@login_required
def resend_confirmation_email():
    token = current_user.generate_account_confirmation_token()
    send_email(current_user.email,
               'Confirm your Hedgehog Account',
               '/auth/email/confirmation',
               user=current_user,
               token=token)
    flash('Confirmation email has been resent.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Password', 'auth/email/reset_password', user=user, token=token)
    flash('An email with instructions to reset your password has been sent to you,')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Password updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('Instructions to confirm your new email address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Email address updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
