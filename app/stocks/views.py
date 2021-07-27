from flask import render_template

from . import stocks


@stocks.route('/stock')
def get_stock_info():


    stocks = [
        {
            'name': 'Tesla',
            'ticker': 'TSLA',
            'description': 'Electric vehicle manufacturer',
            'industry': 'Automotive ',
            'last_trade_price': '13.00',
            '52_week_high': '54.00',
            '52_week_low': '5.00',
            'stretch_goals': 'Goals',
            'todays_growth': '2.14',
            'total_growth': '-4.42',
            'news': 'Elon shot a lazer beam down from space striking a Toyota Rav4 before Andre was able to drop a 50 bomb in fortnite mobile causing him to miss out on legendary status'
         },
        {
            'name': 'Tesla',
            'ticker': 'TSLA',
            'description': 'Electric vehicle manufacturer',
            'industry': 'Automotive ',
            'last_trade_price': '13.00',
            '52_week_high': '54.00',
            '52_week_low': '5.00',
            'stretch_goals': 'Goals',
            'todays_growth': '2.14',
            'total_growth': '-4.42',
            'news': 'Elon shot a lazer beam down from space striking a Toyota Rav4 before Andre was able to drop a 50 bomb in fortnite mobile causing him to miss out on legendary status'
         },
        {
            'name': 'Tesla',
            'ticker': 'TSLA',
            'description': 'Electric vehicle manufacturer',
            'industry': 'Automotive ',
            'last_trade_price': '13.00',
            '52_week_high': '54.00',
            '52_week_low': '5.00',
            'stretch_goals': 'Goals',
            'todays_growth': '2.14',
            'total_growth': '-4.42',
            'news': 'Elon shot a lazer beam down from space striking a Toyota Rav4 before Andre was able to drop a 50 bomb in fortnite mobile causing him to miss out on legendary status'
         },
        {
            'name': 'Tesla',
            'ticker': 'TSLA',
            'description': 'Electric vehicle manufacturer',
            'industry': 'Automotive ',
            'last_trade_price': '13.00',
            '52_week_high': '54.00',
            '52_week_low': '5.00',
            'stretch_goals': 'Goals',
            'todays_growth': '2.14',
            'total_growth': '-4.42',
            'news': 'Elon shot a lazer beam down from space striking a Toyota Rav4 before Andre was able to drop a 50 bomb in fortnite mobile causing him to miss out on legendary status'
         },
        {
            'name': 'Tesla',
            'ticker': 'TSLA',
            'description': 'Electric vehicle manufacturer',
            'industry': 'Automotive ',
            'last_trade_price': '13.00',
            'fifty_two_week_high': '54.00',
            'fifty_two_week_low': '5.00',
            'stretch_goals': 'Goals',
            'todays_growth': '2.14',
            'total_growth': '-4.42',
            'news': 'Elon shot a lazer beam down from space striking a Toyota Rav4 before Andre was able to drop a 50 bomb in fortnite mobile causing him to miss out on legendary status'
         }

    ]
    return render_template('stocks/stock_info.html', stocks=stocks)
