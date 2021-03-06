# -*- coding: utf-8 -*-

from flask import Markup

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import AnyOf
from flask.ext.wtf import (HiddenField, BooleanField, TextField, RadioField,
        PasswordField, SubmitField)
from flask.ext.wtf import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from flaskext.babel import lazy_gettext as _

from ..user import User, USER_LOCALE_STRING, USER_LOCALE_ZH_CN
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)


class LoginForm(Form):
    next = HiddenField()
    login = TextField(_(u'Username or email'), [Required()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    locale_code = RadioField(_("Language"), [AnyOf([str(val) for val in USER_LOCALE_STRING.keys()])],
            choices=[(str(val), label) for val, label in USER_LOCALE_STRING.items()], default=USER_LOCALE_ZH_CN)
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Login'))


class SignupForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    agree = BooleanField(u'Agree to the ' +
        Markup('<a target="blank" href="/terms">Terms of Service</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')


class RecoverPasswordForm(Form):
    email = EmailField(u'Your email', [Email()])
    submit = SubmitField('Send instructions')


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(u'Password', [Required()])
    password_again = PasswordField(u'Password again', [EqualTo('password', message="Passwords don't match")])
    submit = SubmitField('Save')


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField('Reauthenticate')


class OpenIDForm(Form):
    openid = TextField(u'Your OpenID', [Required()])
    submit = SubmitField(u'Log in with OpenID')


class CreateProfileForm(Form):
    openid = HiddenField()
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    email = EmailField(u'Email', [Required(), Email()], description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    submit = SubmitField(u'Create Profile')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken.')
