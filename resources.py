# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xad\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\
\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc3\x00\x00\x0e\xc3\
\x01\xc7\x6f\xa8\x64\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\
\x74\x77\x61\x72\x65\x00\x77\x77\x77\x2e\x69\x6e\x6b\x73\x63\x61\
\x70\x65\x2e\x6f\x72\x67\x9b\xee\x3c\x1a\x00\x00\x00\x3a\x49\x44\
\x41\x54\x38\x8d\x63\x64\x60\x60\xf8\xcf\x40\x01\x60\xa2\x44\xf3\
\x30\x31\x80\x25\x2c\x2c\xec\x1c\x25\x06\x30\xfe\xff\xff\x7f\xa4\
\xc7\x02\xcb\xf9\xf3\xe7\x4f\x51\x64\xc0\xa6\x4d\x9b\xcc\x28\x31\
\x60\xe0\xc3\x60\xe0\x0d\x00\x00\x39\x11\x0c\x73\x1c\x8d\x89\x1f\
\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x07\
\x07\x3b\xe0\xb3\
\x00\x70\
\x00\x6c\x00\x75\x00\x67\x00\x69\x00\x6e\x00\x73\
\x00\x13\
\x02\xeb\x2a\x82\
\x00\x62\
\x00\x61\x00\x63\x00\x6b\x00\x67\x00\x72\x00\x6f\x00\x75\x00\x6e\x00\x64\x00\x5f\x00\x73\x00\x77\x00\x69\x00\x74\x00\x63\x00\x68\
\x00\x65\x00\x72\
\x00\x08\
\x0a\x61\x5a\xa7\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x14\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x40\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x14\x00\x02\x00\x00\x00\x01\x00\x00\x00\x03\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x40\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x8e\x2b\x3c\xf9\xd0\
"

qt_version = [int(v) for v in QtCore.qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    QtCore.qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
