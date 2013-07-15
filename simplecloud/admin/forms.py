# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, RadioField, DateField, 
        PasswordField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange
from flask.ext.wtf.html5 import EmailField, IntegerField

from ..user import USER_ROLE, USER_STATUS
from ..user import User
from .constants import HOST_TYPE
from .models import Host, Image, Task, Template
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, VM_QUOTA_MIN, VM_QUOTA_MAX,
        VCPU_NUM_MIN, VCPU_NUM_MAX, MEM_SIZE_MIN, MEM_SIZE_MAX, 
        DISK_SIZE_MIN, DISK_SIZE_MAX)

# User Form
class AddUserForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    submit = SubmitField(u'Save')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')

class EditUserForm(Form):
    next = HiddenField()    
    name = TextField(u'User Name', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)])
    role_code = RadioField(u"Role", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    vm_quota = IntegerField(u"VM Quota", [Required(), NumberRange(VM_QUOTA_MIN, VM_QUOTA_MAX)])
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')
    
    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

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

# Image Form    
class AddImageForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the image name', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    src_path = TextField(u'Choose the image file path', [Required()],
            description=u"The image will be copied to IMAGEPOOL from this location.")

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Image.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This image name is taken')

# Image not support edit 
'''
class EditImageForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the image name', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Image.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This image name is taken')
'''
            
# Template Form
class AddTemplateForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the template name', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    image_id = IntegerField(u'Choose the image attached on this template', [Required()])
    vcpu_desc = "Choose the VCPU number (From " + str(VCPU_NUM_MIN) + " to " + str(VCPU_NUM_MAX) +")"
    vcpu = IntegerField(unicode(vcpu_desc), [Required(), NumberRange(VCPU_NUM_MIN, VCPU_NUM_MAX)])
    memory_desc = "Choose the Memory size (From " + str(MEM_SIZE_MIN) + "M to " + str(MEM_SIZE_MAX) +"M)"
    memory = IntegerField(unicode(memory_desc), [Required(), NumberRange(MEM_SIZE_MIN, MEM_SIZE_MAX)])
    disk_desc = "Choose the Disk size (From " + str(DISK_SIZE_MIN) + "M to " + str(DISK_SIZE_MAX) +"M)"
    disk = IntegerField(unicode(disk_desc), [Required(), NumberRange(DISK_SIZE_MIN, DISK_SIZE_MAX)])

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Template.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This template name is taken')
            
    def validate_image_id(self, field):
        if Image.query.filter_by(id=field.data).first() is None:
            raise ValidationError(u'This Image is not found')

# Template not support edit
# class EditTemplateForm(Form)



