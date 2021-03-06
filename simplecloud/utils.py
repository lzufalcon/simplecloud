# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

import string
import random
import os
import shutil

from datetime import datetime

# Instance folder path, make it independent.
INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')
INSTANCE_CONFIG_PATH = os.path.join(INSTANCE_FOLDER_PATH, 'config')

# XML Config file
XML_CONFIG_FILE = os.path.join(INSTANCE_CONFIG_PATH, 'vm.xml')

SHARED_STORAGE_PATH = os.path.join(INSTANCE_FOLDER_PATH, "share")
IMAGE_POOL_PATH = os.path.join(SHARED_STORAGE_PATH, 'images')
VM_POOL_PATH = os.path.join(SHARED_STORAGE_PATH, 'vms')

# Host configuraiton
HOST_PUBKEY_FILE = "/root/.ssh/id_rsa.pub"

# Storage Configuration
STORAGE_TYPE = "Shared"
STORAGE_PROTOCOL = "NFS"

# Network Configuration
NETWORK_MODE = "NAT"
VM_NETWORK_MODE = "DHCP"
NETWORK_NAME = "default"

# Form validation

USERNAME_LEN_MIN = 4
USERNAME_LEN_MAX = 25

REALNAME_LEN_MIN = 4
REALNAME_LEN_MAX = 25

PASSWORD_LEN_MIN = 6
PASSWORD_LEN_MAX = 16

VM_QUOTA_MIN = 0
VM_QUOTA_MAX = 10

VCPU_NUM_MIN = 1
VCPU_NUM_MAX = 4

MEM_SIZE_MIN = 64
MEM_SIZE_MAX = 4096

DISK_SIZE_MIN = 128
DISK_SIZE_MAX = 102400

# Model
STRING_LEN = 64
NAME_LEN_MIN = 4
NAME_LEN_MAX = STRING_LEN

def get_current_time():
    return datetime.utcnow()

def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

def id_generator(size=10, chars=string.ascii_letters + string.digits):
    #return base64.urlsafe_b64encode(os.urandom(size))
    return ''.join(random.choice(chars) for x in range(size))

def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception, e:
        raise e

def get_xml_file():
    with open(XML_CONFIG_FILE, 'r') as content_file:
	content = content_file.read()

    return content

def copy_file(src, dst):
    shutil.copy2(src, dst)

