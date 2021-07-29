from datetime import datetime

from flask import abort, current_app, flash, render_template, session, redirect, request, url_for
from flask_login import current_user, login_required
from . import main
from .forms import BuyStockForm, EditProfileAdministratorForm, EditProfileForm
from .. import db
from ..decorators import admin_required
from ..models import Permission, Role, Stock, Trade, User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = BuyStockForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        trade = Trade(stock=Stock.query.filter_by(ticker=form.ticker.data).first(),
                      price=form.price.data,
                      quantity=form.quantity.data,
                      user=current_user._get_current_object())
        db.session.add(trade)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Trade.query.order_by(Trade.timestamp.desc()).paginate(
        page, per_page=current_app.config['INDEX_POSTS_PER_PAGE'],
        error_out=False)
    trades = pagination.items
    return render_template('index.html', form=form, trades=trades, pagination=trades)


@main.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(user_id):
    edit_user = User.query.get_or_404(user_id)
    form = EditProfileAdministratorForm(user=edit_user)
    if form.validate_on_submit():
        edit_user.about_me = form.about_me.data
        edit_user.confirmed = form.confirmed.data
        edit_user.email = form.email.data
        edit_user.location = form.location.data
        edit_user.name = form.name.data
        edit_user.role = Role.query.get(form.role.data)
        edit_user.username = form.username.data
        db.session.add(edit_user)
        db.session.commit()
        flash('Profile for ' + edit_user.username + ' updated successfully.')
        return redirect(url_for('.user_profile', username=edit_user.username))
    form.about_me.data = edit_user.about_me
    form.confirmed.data = edit_user.confirmed
    form.email.data = edit_user.email
    form.location.data = edit_user.location
    form.name.data = edit_user.name
    form.role.data = edit_user.role_id
    form.username.data = edit_user.username
    return render_template('edit_profile.html', form=form, user=edit_user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # Save submitted form
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        current_user.name = form.name.data
        db.session.add(current_user)
        db.session.commit()
        flash('Profile successfully updated.')
        return redirect(url_for('.user_profile', username=current_user.username))
    # Populate form with user data
    form.about_me.data = current_user.about_me
    form.location.data = current_user.location
    form.name.data = current_user.name
    return render_template('edit_profile.html', form=form)


@main.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    trades = user.trades.order_by(Trade.timestamp.desc()).all()
    return render_template('user_profile.html', user=user, trades=trades)


@main.route('/shutdown')
def server_shutdown():
    """Used by unit tests to stop flask server"""
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
