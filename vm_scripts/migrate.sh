#!/bin/sh

if [ $# == 2 ];then
  vm_name=$1
  KVM_IP=$2
  if [ `lvs 2>/dev/null| grep s_$vm_name | awk '{print $5}'|awk -F '_' '{print $1}'| grep -v "^$"` == "centos" ];then
    ssh root@$KVM_IP "lvcreate -L +2G -n s_$vm_name vg01"
  else
    ssh root@$KVM_IP "lvcreate -L +1G -n s_$vm_name vg01"	
  fi
  virsh migrate --verbose --live --persistent s_$vm_name qemu+ssh://$KVM_IP/system
  ssh root@$KVM_IP "virsh dumpxml s_$vm_name > /data/vm_xml/s_$vm_name.xml"
else
  echo "enter the vm_name and kvm_ip as the args for migrate."
fi
