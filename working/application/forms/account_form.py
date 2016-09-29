# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    account = EmailField(u'E-Mail', validators=[Email()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    remember = BooleanField(u'Remember')
    submit = SubmitField(u'Submit')
