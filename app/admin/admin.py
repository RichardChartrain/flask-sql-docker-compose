# -*- coding: utf-8 -*-
from flask import request, redirect, url_for
from flask_admin import Admin
from flask_admin.base import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import AdminIndexView
from flask.ext.login import current_user, helpers, login

from app import app
from db import db
from forms import LoginForm
from models import User

# Create a admin object
admin = Admin(app)

# User view for admin
class UserView(ModelView):
    can_delete = False
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


admin.add_view(UserView(User, db.session))
