#!/bin/sh

#每5秒执行一次
#* * * * * sleep 5 && /data/start_vm_vnc.sh &
sshpass -p 'ychina2017@' scp 192.168.0.131:/vm_scripts/vm_list /data/
cd /data/

if [ `cat /data/vm_list | awk -F'|' '{print $1}'|grep -vE "^$| "` == "#" ];then
    break
else
    for ip in `cat /data/vm_list|awk -F'|' '{print $2}'|grep -vE "^$| "`
    do
	if [ `ps -ef | grep launch.sh| grep -v grep|grep $ip|wc -l` == 1 ];then
	    continue
        else
	    port=32`echo $ip| awk -F. '{print $4}'`
	    /data/noVNC-master/utils/launch.sh --vnc $ip:5901 --listen $port &
	fi
    done
fi
