from flask import abort, current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import users
from .forms import EditProfileAdministratorForm, EditProfileForm
from .. import db
from ..decorators import admin_required, permission_required
from ..models import Permission, Role, Trade, User

watchListStocks = [
    {
        "name": "A",
        "ticker": "A",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "300",
        "gainLossSincePurchasePercentage": "30%"
    },
        {
        "name": "B",
        "ticker": "B",
        "lastTrade": "500.00",
        "shares": "2000",
        "purchasePrice": "264.00",
        "currentPrice": "525.00",
        "gainLossSincePurchase": "200",
        "gainLossSincePurchasePercentage": "20%"
    },
        {
        "name": "C",
        "ticker": "C",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "400",
        "gainLossSincePurchasePercentage": "40%"
    },
        {
        "name": "D",
        "ticker": "D",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "900",
        "gainLossSincePurchasePercentage": "90%"
    },
        {
        "name": "E",
        "ticker": "E",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "800",
        "gainLossSincePurchasePercentage": "80%"
    },
        {
        "name": "F",
        "ticker": "F",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "700",
        "gainLossSincePurchasePercentage": "70%"
    },
        {
        "name": "G",
        "ticker": "G",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "100",
        "gainLossSincePurchasePercentage": "10%"
    },
        {
        "name": "H",
        "ticker": "H",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "400",
        "gainLossSincePurchasePercentage": "40%"
    },
        {
        "name": "I",
        "ticker": "I",
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "500",
        "gainLossSincePurchasePercentage": "50%"
    },
        {
        "name": "J",
        "ticker": "J",
        "lastTrade": "500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "525.00",
        "gainLossSincePurchase": "600",
        "gainLossSincePurchasePercentage": "60%"
    }

]

@users.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    #TODO add form=form, stocks=trade_items, pagination=pagination back in if needed
    return render_template('users/watchlist.html', stocks=watchListStocks)


@users.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
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
    return render_template('users/edit_profile.html', form=form, user=edit_user)


@users.route('/edit-profile', methods=['GET', 'POST'])
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
    return render_template('users/edit_profile.html', form=form)


@users.route('/follow/<username>')
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


@users.route('/unfollow/<username>')
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


@users.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('users/followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@users.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config['FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('users/followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@users.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    trades = user.trades.order_by(Trade.timestamp.desc()).all()
    return render_template('users/user_profile.html', user=user, trades=trades)
