from flask import abort, current_app, render_template, flash, redirect, request, url_for
from flask_login import login_required

from . import stocks
from .forms import AddStockForm, EditStockForm
from .. import db
from ..decorators import admin_required
from ..models import Stock, Trade


@stocks.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_stock():
    form = AddStockForm()
    if form.validate_on_submit():
        new_stock = Stock(ticker=form.ticker.data,
                          name=form.name.data,
                          is_active=form.active.data,
                          sector=form.sector.data,
                          year_high=form.year_high.data,
                          year_low=form.year_low.data)
        db.session.add(new_stock)
        db.session.commit()
        flash('Profile for ' + new_stock.name + ' created successfully.')
        return redirect(url_for('.stock_info', ticker=new_stock.ticker))
    return render_template('stocks/edit_stock.html', form=form)


@stocks.route('/edit/<ticker>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stock(ticker):
    stock = Stock.query.filter_by(ticker=ticker).first()
    if stock is None:
        abort(404)
    form = EditStockForm(stock=stock)
    if form.validate_on_submit():
        stock.ticker = form.ticker.data
        stock.name = form.name.data
        stock.is_active = form.active.data
        stock.sector = form.sector.data
        stock.year_high = form.year_high.data
        stock.year_low = form.year_low.data
        db.session.add(stock)
        db.session.commit()
        flash('Profile for ' + stock.name + ' updated successfully.')
        return redirect(url_for('.stock_info', ticker=stock.ticker))
    form.ticker.data = stock.ticker
    form.name.data = stock.name
    form.active.data = stock.is_active
    form.sector.data = stock.sector
    form.year_high.data = stock.year_high
    form.year_low.data = stock.year_low
    return render_template('stocks/edit_stock.html', form=form, stock=stock)


@stocks.route('/<ticker>')
@login_required
def stock_info(ticker):
    stock = Stock.query.filter_by(ticker=ticker).first()
    if stock is None:
        abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = stock.trades.order_by(Trade.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['TRADES_PER_PAGE'],
        error_out=False)
    trades = pagination.items
    return render_template('stocks/stock_info.html', stock=stock, trades=trades, pagination=pagination)
