#!/usr/bin/python

from RedisHelper import RedisHelper

obj = RedisHelper()
vm_name = "xp01"
vm_cpu = 1
vm_memory = 2
vm_disk = 20
vm_images = "windows_xp"
vm_info = [vm_name,vm_cpu,vm_memory,vm_disk,vm_images]
obj.publish(vm_info)
