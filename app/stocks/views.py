from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from . import stocks
from .forms import EditStockForm
from .. import db
from ..decorators import admin_required
from ..models import Stock


@stocks.route('/edit/<int:stock_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_stock(stock_id):
    new_stock = Stock.query.get_or_404(stock_id)
    form = EditStockForm(stock=new_stock)
    if form.validate_on_submit():
        new_stock.ticker = form.ticker.data
        new_stock.name = form.name.data
        new_stock.is_active = form.active.data
        new_stock.sector = form.sector.data
        new_stock.year_high = form.year_high.data
        new_stock.year_low = form.year_low.data
        db.session.add(new_stock)
        db.session.commit()
        flash('Profile for ' + new_stock.name + ' updated successfully.')
        return redirect(url_for('.stock_info', ticker=new_stock.ticker))
    form.ticker.data = new_stock.ticker
    form.name.data = new_stock.name
    form.active.data = new_stock.is_active
    form.sector.data = new_stock.sector
    form.year_high.data = new_stock.year_high
    form.year_low.data = new_stock.year_low
    return render_template('stocks/edit_stock.html', form=form, stock=new_stock)


@stocks.route('/<ticker>')
def stock_info(ticker):
    stock = Stock.query.filter_by(ticker=ticker).first()
    return render_template('stocks/stock_info.html', stock=stock)
