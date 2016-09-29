# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class DaoTokenForm(Form):
    token = StringField(u'API Token', validators=[DataRequired()])

    submit = SubmitField(u'Submit')
