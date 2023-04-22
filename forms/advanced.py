from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired


class AdvancedForm(FlaskForm):
    title = StringField('Title')
    type = StringField('Type')
    place = StringField('Place of creation')
    mattech = StringField('Material or technique')
    people = StringField('Creator or related person')
    year_from = IntegerField('Made in a year ranging from...')
    year_to = IntegerField('...to')
    exist = BooleanField('Every result should have an image')
    on_display_at = SelectField('On display at',
                                choices=[('', 'Any'), ('south_kensington', 'V&A South Kensington'), ('dundee', 'V&A Dundee'),
                                         ('moc', 'V&A Museum of Childhood')])
    order_by = SelectField('Order by',
                                choices=[('', 'No order'), ('date', 'Date'), ('location', 'Display Location'),
                                         ('place', 'Place'), ('artist', 'Artist'), ('fields_populated', 'Amount of data')])
    order_sort = SelectField('Order...',
                                choices=[('', "Don't sort"), ('asc', '...ascending'), ('desc', '...descending')])
    page_size = IntegerField('Objects per page')
    submit = SubmitField('Add parameters')
