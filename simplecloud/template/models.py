# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (TEMPLATE_STATUS, TEMPLATE_OK)
from ..utils import STRING_LEN

class Template(db.Model):

    __tablename__ = 'templates'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    image_id = Column(db.Integer, db.ForeignKey("images.id", ondelete="SET NULL"))
    vms = db.relationship("VM")

    # VCPU number
    vcpu = Column(db.Integer, nullable=False)
    # CPU percentage (100 = 1 physical CPU)
    pcpu = Column(db.Integer, nullable=False)
    # Memory size (M)
    memory = Column(db.Integer, nullable=False)
    # Disk size (M)
    disk = Column(db.Integer, nullable=False)
    # number of VMs created from this template
    vm_number = Column(db.Integer, default=0)

    status_code = Column(db.SmallInteger, default=TEMPLATE_OK)

    @property
    def status(self):
        return TEMPLATE_STATUS[self.status_code]

    @classmethod
    def get_templates_choices(cls):
        template_list = []
        templates = cls.query.filter_by(status_code=TEMPLATE_OK).all()
        for template in templates:
            template_list.append((str(template.id), template.name))
        return template_list

