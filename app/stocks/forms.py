from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError
from ..models import Stock, Trade, User


class EditStockForm(FlaskForm):
    """
    Form for administrators to edit stock information
    Rendered by wtf.quick_form()
    """
    ticker = StringField('Ticker', validators=[DataRequired(), Length(1, 5)])
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    active = BooleanField('Active')
    sector = StringField('Sector', validators=[DataRequired(), Length(1, 32)])
    year_high = DecimalField('52-Week High', places=2, validators=[DataRequired()])
    year_low = DecimalField('52-Week Low', places=2, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, stock, *args, **kwargs):
        super(EditStockForm, self).__init__(*args, **kwargs)
        self.stock = stock

    def validate_ticker(self, field):
        if field.data != self.stock.ticker and Stock.query.filter_by(ticker=field.data).first():
            raise ValidationError('Ticker already in use.')

    def validate_year_high(self, field):
        if field.data < 0:
            raise ValidationError('52-Week High cannot be negative.')
        elif field.data < self.year_low.data:
            raise ValidationError('52-Week High cannot be > 52-Week Low.')

    def validate_year_low(self, field):
        if field.data < 0:
            raise ValidationError('52-Week Low cannot be negative.')
        elif field.data > self.year_high.data:
            raise ValidationError('52-Week Low cannot be > 52-Week High.')
