from flask import render_template

from . import stocks


@stocks.route('/stock')
def get_stock_info():
    stock = {'name': 'Tesla', 'ticker': 'TSLA', 'last_trade_price': '13.00'}
    return render_template('stocks/stock_info.html', stock=stock)
