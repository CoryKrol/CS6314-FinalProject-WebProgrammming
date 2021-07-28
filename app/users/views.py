from flask import render_template

from . import stocks


@stocks.route('/user')
def get_user_info():
    return render_template('users/user_info.html')
