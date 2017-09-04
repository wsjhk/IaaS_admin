#!/bin/sh

if [ $# == 1 ];then
    disk_name=$1
    if [ `grep $disk_name /vm_scripts/disk_list|awk -F '|' '{print $3}'` == "unuse" ];then
	rm -f /data/vm_disk/vm_$disk_name.img /data/vm_disk/vm_$disk_name.xml
	sed -i "/$disk_name/"d /vm_scripts/disk_list
    else
	vm_name=`grep $disk_name /vm_scripts/disk_list|awk -F '|' '{print $3}'`
	virsh detach-device s_$vm_name /data/vm_disk/vm_$disk_name.xml
	rm -f /data/vm_disk/vm_$disk_name.img /data/vm_disk/vm_$disk_name.xml
	sed -i "/$disk_name/"d /vm_scripts/disk_list
    fi
else
    echo "enter a disk_name as a args."
fi

