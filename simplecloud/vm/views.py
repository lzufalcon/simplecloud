# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user
from flaskext.babel import gettext as _

from ..extensions import db
from .models import VM
from .forms import AddVMForm
from .utils import VMAction, create_vm
from ..task import log_task, TASK_FAILED
from ..template import Template

vm = Blueprint('vm', __name__, url_prefix='/vms')

# List/Create VM
@vm.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    if current_user.is_admin():
        vms = VM.query.filter().all()
    else:
        vms = VM.query.filter(VM.owner_id == current_user.id).all()

    form = AddVMForm(next=request.args.get('next'))
    form.template_id.choices = Template.get_templates_choices()
    
    if form.validate_on_submit():
        vm = VM()
        form.populate_obj(vm)
        # validate VM name here
        if VM.query.filter(db.and_(VM.owner_id == current_user.id,
                VM.name == vm.name)).first() is not None:
            flash(_("VM Name %(name)s is taken.", name = vm.name), "error")
            return redirect(form.next.data or url_for('user.index'))
        vm.owner_id = current_user.id
        create_vm(vm)
        return redirect(form.next.data or url_for('vm.index'))
    elif form.is_submitted():
        flash(_("Failed to add VM"), "error")
      
    return render_template('vm/index.html', vms=vms, form=form, active=_("VirtualMachines"))
    
# VM action Page    
@vm.route('/<action>/<int:vm_id>', methods=['GET'])
@login_required
def do(action, vm_id):
    vm = VM.query.filter_by(id=vm_id).first_or_404()
    vmaction = VMAction()
    op = getattr(vmaction, action, None)
    if callable(op):
        op(vm)
    else:
        errMsg = _("Not supported action %(name)s", name = action)
        flash(errMsg, "error")
    return redirect(url_for("vm.index"))



