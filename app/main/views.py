from flask import abort, current_app, flash, make_response, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import main
from .forms import EditProfileAdministratorForm, EditProfileForm
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Role, Trade, User


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    show_followed_trades = False
    if current_user.is_authenticated:
        show_followed_trades = bool(request.cookies.get('show_followed_trades', ''))
    if show_followed_trades:
        query = current_user.followed_trades
    else:
        query = Trade.query
    pagination = query.order_by(Trade.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['TRADES_PER_PAGE'], error_out=False)
    trades = pagination.items
    return render_template('index.html',
                           trades=trades,
                           show_followed_trades=show_followed_trades,
                           pagination=pagination)


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


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('Already following user.')
        return redirect(url_for('.user_profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user_profile', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('Not following user.')
        return redirect(url_for('.user_profile', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user_profile', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    trades = user.trades.order_by(Trade.timestamp.desc()).all()
    return render_template('user_profile.html', user=user, trades=trades)


@main.route('/all')
@login_required
def show_all():
    """
    Cookies can only be set using responses, have to do it here instead of letting flask set it
    max_age is in seconds, without setting it the cookie expires when the browser closes
    """
    response = make_response(redirect(url_for('.index')))
    response.set_cookie('show_followed_trades', '', max_age=30*24*60*60)
    return response


@main.route('/followed')
@login_required
def show_followed():
    """
    Cookies can only be set using responses, have to do it here instead of letting flask set it
    max_age is in seconds, without setting it the cookie expires when the browser closes
    """
    response = make_response(redirect(url_for('.index')))
    response.set_cookie('show_followed_trades', '1', max_age=30*24*60*60)
    return response


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
