from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Trade


@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_json())


@api.route('/users/<int:user_id>/trades/')
def get_user_trades(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.trades.order_by(Trade.timestamp.desc()).paginate(
        page, per_page=current_app.config['TRADES_PER_PAGE'],
        error_out=False)
    trades = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_trades', id=id, page=page-1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_user_trades', id=id, page=page+1)
    return jsonify({
        'trades': [trade.to_json() for trade in trades],
        'prev': prev,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/users/<int:user_id>/timeline/')
def get_user_followed_trades(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_trades.order_by(Trade.timestamp.desc()).paginate(
        page, per_page=current_app.config['TRADES_PER_PAGE'],
        error_out=False)
    trades = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_trades', id=id, page=page-1)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_user_followed_trades', id=id, page=page+1)
    return jsonify({
        'trades': [trade.to_json() for trade in trades],
        'prev': prev,
        'next': next_page,
        'count': pagination.total
    })
