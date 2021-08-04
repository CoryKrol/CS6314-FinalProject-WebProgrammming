from flask import current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import trades
from .forms import BuyStockForm, EditTradeForm
from .. import db
from ..decorators import admin_required
from ..models import Permission, Stock, Trade, User


@trades.route('/edit/<int:trade_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_trade(trade_id):
    trade_object = Trade.query.get_or_404(trade_id)
    form = EditTradeForm(trade=trade_object)
    if form.validate_on_submit():
        trade_object.stock = Stock.query.filter_by(ticker=form.ticker.data).first()
        trade_object.price = form.price.data
        trade_object.quantity = form.quantity.data
        trade_object.user = User.query.filter_by(username=form.user.data).first()
        db.session.add(trade_object)
        db.session.commit()
        flash('Information for Trade #' + str(trade_object.id) + ' updated successfully.')
        return redirect(url_for('.trade', trade_id=trade_id))
    form.ticker.data = trade_object.stock.ticker
    form.price.data = trade_object.price
    form.quantity.data = trade_object.quantity
    form.user.data = trade_object.user.username
    return render_template('trades/edit_trade.html', form=form, trade=trade)


# noinspection PyProtectedMember
@trades.route('/', methods=['GET', 'POST'])
@login_required
def trades_list():
    form = BuyStockForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        trade_object = Trade(stock=Stock.query.filter_by(ticker=form.ticker.data).first(),
                             price=form.price.data,
                             quantity=form.quantity.data,
                             user=current_user._get_current_object())
        db.session.add(trade_object)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Trade.query.order_by(Trade.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['TRADES_PER_PAGE'],
        error_out=False)
    trade_items = pagination.items
    return render_template('index.html', form=form, trades=trade_items, pagination=pagination)


@trades.route('/<int:trade_id>')
@login_required
def trade(trade_id):
    trade_object = Trade.query.get_or_404(trade_id)
    return render_template('trades/trade.html', trades=[trade_object])
