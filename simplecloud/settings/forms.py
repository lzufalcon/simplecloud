# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, TextField, AnyOf, Optional,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField)
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange, URL
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX, AGE_MIN, AGE_MAX, DEPOSIT_MIN, DEPOSIT_MAX
from ..utils import allowed_file, ALLOWED_AVATAR_EXTENSIONS
from ..utils import SEX_TYPE


class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()])
    username = TextField(u'Username', [Length(max=64)])
    quota = TextField(u'Quota', [Length(max=64)])
    submit = SubmitField(u'Save')

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError("Please pick another name.")

    def validate_avatar_file(form, field):
        if field.data and not allowed_file(field.data.filename):
            raise ValidationError("Please upload files with extensions: %s" % "/".join(ALLOWED_AVATAR_EXTENSIONS))


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Current password', [Required()])
    new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(u'Save')

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError("Password is wrong.")