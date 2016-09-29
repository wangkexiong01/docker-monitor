# -*- coding: utf-8 -*-

from application.extensions import db


class DaoToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(128), index=True, unique=True)
    token = db.Column(db.String(50))
