from flask import render_template

from . import users


@users.route('/user')
def get_user_positions():
    return render_template('users/user_positions.html')
