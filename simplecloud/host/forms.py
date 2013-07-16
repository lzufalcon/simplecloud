# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField, RadioField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX)
from .constants import HOST_TYPE
from .models import Host
     

# Host Form    
class AddHostForm(Form):
    next = HiddenField()
    address = TextField(u'The IP address or hostname of target host', [Required()])
    type_code = RadioField(u"Hypervisor Type", [AnyOf([str(val) for val in HOST_TYPE.keys()])],
            choices=[(str(val), label) for val, label in HOST_TYPE.items()])
    
    username = TextField(u'The Username used by libvirt+ssh connection', [Required()])

    submit = SubmitField(u'Save')

    def validate_address(self, field):
        if Host.query.filter_by(address=field.data).first() is not None:
            raise ValidationError(u'This host is added')

class EditHostForm(Form):
    next = HiddenField()
    type_code = RadioField(u"Hypervisor Type", [AnyOf([str(val) for val in HOST_TYPE.keys()])],
            choices=[(str(val), label) for val, label in HOST_TYPE.items()])
    username = TextField(u'The Username used by libvirt+ssh connection', [Required()])
    submit = SubmitField(u'Save')
    def validate_address(self, field):
        if Host.query.filter_by(address=field.data).first() is not None:
            raise ValidationError(u'This host is added')


