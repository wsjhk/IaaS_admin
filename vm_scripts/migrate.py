#!/usr/bin/python

import libvirt
import pprint
conn_01 = libvirt.open('qemu+tcp://vm01/system')
conn_02 = libvirt.open('qemu+tcp://vm02/system')
vm_domain = conn_01.lookupByName('s_migrate')
vm_domain.migrate(conn_02,True,'s_migrate',None,0)
pprint.pprint(help(vm_domain.migrate))

