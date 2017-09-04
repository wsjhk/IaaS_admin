#!/bin/sh

if [ $# == 2 ];then
disk_name=$1
disk_size=$2
flag=${disk_name: -1}
qemu-img create -f qcow2 /data/vm_disk/vm_$1.img $2G

echo "
<disk type='file' device='disk'>
	<driver name='qemu' type='qcow2'/>
	<source file='/data/vm_disk/vm_$1.img'/>
	<target dev='hd$flag' bus='virtio' type='virtio'/>
</disk>" > /data/vm_disk/vm_$1.xml
echo "$disk_name|$disk_size|unuse" >> /vm_scripts/disk_list
else
echo "the args is error,please enter the disk_name and disk_size."
fi

