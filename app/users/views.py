from flask import current_app, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from . import users
from .. import db
from ..decorators import admin_required
from ..models import Permission, Stock, Trade, User

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
        "lastTrade": "1500.00",
        "shares": "2000",
        "purchasePrice": "1264.00",
        "currentPrice": "1525.00",
        "gainLossSincePurchase": "600",
        "gainLossSincePurchasePercentage": "60%"
    },

]

@users.route('/watchlist', methods=['GET', 'POST'])
@login_required
def watchlist():
    #TODO add form=form, stocks=trade_items, pagination=pagination back in if needed
    return render_template('users/watchlist.html', stocks=watchListStocks)