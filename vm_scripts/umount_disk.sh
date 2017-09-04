#!/bin/sh

if [ $# == 1 ];then
    disk_name=$1
    vm_name=`grep $disk_name /vm_scripts/disk_list|awk -F '|' '{print $3}'`
    virsh detach-device s_$vm_name /data/vm_disk/vm_$disk_name.xml
    sed -i "s/$disk_name|\(.*\)|.*/$disk_name|\1|unuse/g" /vm_scripts/disk_list
else
    echo "enter a disk_name as a args."
fi
