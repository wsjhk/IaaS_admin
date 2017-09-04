#!/bin/sh

if [ $# == 2 ];then
    vm_name=$1
    disk_name=$2
    virsh attach-device s_$vm_name /data/vm_disk/vm_$disk_name.xml
    sed -i "s/$disk_name|\(.*\)|.*/$disk_name|\1|$vm_name/g" /vm_scripts/disk_list
else
    echo "enter the vm_name and disk_name as the args."
fi
