from flask import abort, current_app, flash, make_response, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import main
from ..models import Trade


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
