# -*- coding: utf-8 -*-

from application.forms import LoginForm
from application.helper import render

from flask import Blueprint, request

account = Blueprint('account', __name__)


@account.route('/', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.account.data
            password = form.password.data
            remember = form.remember.data
            print email, password, remember

    return render('account/login.html', form=form)
