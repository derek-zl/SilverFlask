from flask.ext.login import UserMixin, AnonymousUserMixin
from flask import current_app
from flask_user import UserMixin
from silverflask import user_manager
from silverflask import db
from sqlalchemy.orm import synonym
from . import DataObject
from wtforms import fields, validators



class User(DataObject, UserMixin, db.Model):
    """
    The base User model.
    """
    password = db.Column(db.String)
    username = db.Column(db.String, unique=True)

    email = db.Column(db.String, unique=True)
    
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    
    confirmed_at = db.Column(db.DateTime)
    is_enabled = db.Column(db.Boolean(), nullable=False, server_default='1') 

    roles = db.relationship('Role', secondary='user_roles',
                             backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, email=None, is_enabled=True):
        self.username = username
        self.password = current_app.user_manager.hash_password(password)
        self.email = email
        self.is_enabled = is_enabled

    @property
    def name(self):
        return str(self.firstname) + " " + str(self.lastname)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, new_password):
        self.password = user_manager.hash_password(new_password)

    def as_dict(self):
        d = super().as_dict()
        if d["password"]:
            del d["password"]
        d.update({"name": self.name})
        return d

    @classmethod
    def get_cms_form(cls):
        form = super().get_cms_form()
        if form.password:
            del form.password
        form.new_password = fields.PasswordField("New Password", [validators.EqualTo('new_password_confirmation', message='Passwords must match')])
        form.new_password_confirmation = fields.PasswordField("Repeat New Password")
        return form

class Role(DataObject, db.Model):
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name, description):
        self.name = name
        self.description = description


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
