from ..models import Role, User
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from ..models import Permission, Role, Stock, Trade, User


class BuyStockForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired(), Length(1, 5)])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_price(self, field):
        if field.data < 0:
            raise ValidationError('Price cannot be negative.')

    def validate_quantity(self, field):
        if field.data < 1:
            raise ValidationError('Cannot buy less than 0 shares.')

    def validate_ticker(self, field):
        """TODO: Send email to admin to add stock manually"""
        if not Stock.query.filter_by(ticker=field.data).first():
            raise ValidationError('Stock not in system. An administrator has been notified.')


class EditProfileAdministratorForm(FlaskForm):
    """
    Form for administrators to edit user profiles
    Rendered by wtf.quick_form()
    """
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(1, 64),
                                       Regexp(
                                           '^[A-Za-z][A-Za-z0-9_.]*$',
                                           0,
                                           'Usernames must have only letters, numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdministratorForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class EditProfileForm(FlaskForm):
    """
    Form for users edit their profile
    Rendered by wtf.quick_form()
    """
    name = StringField('Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField()
