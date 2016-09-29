# -*- coding: utf-8 -*-

from ..forms import DaoTokenForm
from ..models import DaoToken
from ..extensions import db
from ..helper import render

from flask import Blueprint, request

daocloud = Blueprint('daocloud', __name__)


@daocloud.route('/', methods=('GET', 'POST'))
def token():
    form = DaoTokenForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            token = form.token.data
            data = DaoToken()
            data.account = 'wangkexiong'
            data.token = token
            db.session.add(data)
            db.session.commit()

    return render('daocloud/_token.html', form=form)
