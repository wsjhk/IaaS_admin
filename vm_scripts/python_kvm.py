#!/usr/bin/python

import subprocess, datetime, os, sys
from os.path import basename
from RedisHelper import RedisHelper

def run_command(cmd):
    if type(cmd) == str:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    else:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    output, err = p.communicate()
    p_status = p.wait()
    result = {"out": output, "err": err, "exit_code": p_status}
    return result

def proform(info):
    vm_name = info[0].split("'")[1]
    cpu = info[1].split("'")[1]
    mem = str(int(info[2].split("'")[1]) * 1024 * 1000)
    disk = info[3].split("'")[1]
    os_type = info[4].split("'")[1]
    print vm_name + cpu + mem + disk + os_type
    if os_type == "Linux_CentOS":
        deploy_cmd = "lvcreate -s -L 2G -n s_%s /dev/vg01/centos_mupan 2>/dev/null && /vm_scripts/create_linux_vm_xml.sh s_%s %s %s && virsh define /data/vm_xml/s_%s.xml && virsh start s_%s" % (vm_name,vm_name,cpu,mem,vm_name,vm_name)
    else:
	deploy_cmd = "lvcreate -s -L 1G -n s_%s /dev/vg01/winxp_mupan 2>/dev/null && /vm_scripts/create_window_vm_xml.sh s_%s %s %s && virsh define /data/vm_xml/s_%s.xml && virsh start s_%s" % (vm_name,vm_name,cpu,mem,vm_name,vm_name)

    DEPLOY_START_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    res = run_command(deploy_cmd)
    if res["exit_code"] == 0:
        DEPLOY_END_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print "Deploy operation successfully."
	write_vm_info_to_file = "echo %s %s %s %s %s running >> /vm_scripts/vm_info.list" % (vm_name,cpu,mem,disk,os_type)
	run_command(write_vm_info_to_file)
        result = "ok"
	return result
    else:
        DEPLOY_END_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print "Deploy operation failure."
        result = "failure"
	return result

if __name__ == "__main__":
    sub = RedisHelper()
    redis_sub = sub.subscribe()
    while 1 < 2:
	msg = redis_sub.parse_response()
	#info = msg[2].split("[")[1].split("]")[0].split(",|'")
        #vm_info = info[0].split(",")
	print msg[2]
	if msg[2] == "vm_list":
	    run_command("/vm_scripts/get_running_vm_info.sh")
	    f = open('/vm_scripts/vm_list', 'r')
	    vm_list = [line.strip() for line in f.readlines()]
	    f.close
            pub = RedisHelper()
            pub.publish(vm_list)
	elif msg[2].split("~")[0] == "delvm":
	    vm_name = msg[2].split("~")[1]
	    if vm_name == "#":
	        run_command("/vm_scripts/get_running_vm_info.sh")
                f = open('/vm_scripts/vm_list', 'r')
                vm_list = [line.strip() for line in f.readlines()]
                f.close
	    else:
		delete_vm = "/vm_scripts/delete_vm.sh %s" % (vm_name)
                run_command(delete_vm)
                run_command("/vm_scripts/get_running_vm_info.sh")
                f = open('/vm_scripts/vm_list', 'r')
                vm_list = [line.strip() for line in f.readlines()]
                f.close
	    pub = RedisHelper()
            pub.publish(vm_list)
	elif msg[2].split("~")[0] == "migrate":
            KVM_IP = msg[2].split("~")[1]
            vm_name = msg[2].split("~")[2]
            migrate_oprate = "/vm_scripts/migrate.sh %s %s" % (vm_name,KVM_IP)
            res = run_command(migrate_oprate)
            print res
	    pub = RedisHelper()
            if res["exit_code"] == 0:
                pub.publish("ok")
            else:
                pub.publish("error")
	elif msg[2].split("~")[0] == "deldisk":
	    disk_name = msg[2].split("~")[1]
            if disk_name == "#":
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            else:
                delete_disk = "/vm_scripts/delete_disk.sh %s" % (disk_name)
                run_command(delete_disk)
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            pub = RedisHelper()
            pub.publish(disk_list)
	elif msg[2].split("~")[0] == "umount":
            disk_name = msg[2].split("~")[1]
            if disk_name == "#":
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            else:
                umount_disk = "/vm_scripts/umount_disk.sh %s" % (disk_name)
                run_command(umount_disk)
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            pub = RedisHelper()
            pub.publish(disk_list)
	elif msg[2].split("~")[0] == "mount":
            disk_name = msg[2].split("~")[1]
            if disk_name == "#":
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            else:
		vm_name = msg[2].split("~")[2]
                mount_disk = "/vm_scripts/mount_disk.sh %s %s" % (vm_name,disk_name)
                run_command(mount_disk)
                run_command("/vm_scripts/get_disk_info.sh")
                f = open('/vm_scripts/disk_list', 'r')
                disk_list = [line.strip() for line in f.readlines()]
                f.close
            pub = RedisHelper()
            pub.publish(disk_list)
	elif msg[2] == "disk_list":
	    run_command("/vm_scripts/get_disk_info.sh")
            f = open('/vm_scripts/disk_list', 'r')
            disk_list = [line.strip() for line in f.readlines()]
            f.close
            pub = RedisHelper()
            pub.publish(disk_list)
	elif msg[2].split("~")[0] == "start":
            vm_name = msg[2].split("~")[1]
            vm_start_oprate = "virsh start s_%s" % (vm_name)
            res = run_command(vm_start_oprate)
            pub = RedisHelper()
            if res["exit_code"] == 0:
                pub.publish("ok")
            else:
                pub.publish("error")
        elif msg[2].split("~")[0] == "shutdown":
            vm_name = msg[2].split("~")[1]
            vm_shutdown_oprate = "virsh shutdown s_%s" % (vm_name)
            res = run_command(vm_shutdown_oprate)
            pub = RedisHelper()
            if res["exit_code"] == 0:
                pub.publish("ok")
            else:
                pub.publish("error")
        elif msg[2].split("~")[0] == "reboot":
            vm_name = msg[2].split("~")[1]
            vm_reboot_oprate = "virsh reboot s_%s" % (vm_name)
            res = run_command(vm_reboot_oprate)
            pub = RedisHelper()
            if res["exit_code"] == 0:
                pub.publish("ok")
            else:
                pub.publish("error")
        elif msg[2].split("~")[0] == "reboot_force":
            vm_name = msg[2].split("~")[1]
            vm_reboot_f_oprate = "virsh destroy s_%s && virsh start s_%s" % (vm_name,vm_name)
            res = run_command(vm_reboot_f_oprate)
	    pub = RedisHelper()
            if res["exit_code"] == 0:
                pub.publish("ok")
            else:
                pub.publish("error")
	elif msg[2].split("~")[0] == "alter":
            vm_name = msg[2].split("~")[1]
	    cpu = msg[2].split("~")[2]
	    ram = msg[2].split("~")[3]
            alter_vm = "virsh setvcpus s_%s %s && virsh setmem s_%s %s && sed -i \"s/<currentMemory unit='KiB'>.*<\/currentMemory>/<currentMemory unit='KiB'>%s<\/currentMemory>/g\" /data/vm_xml/s_centos.xml && sed -i \"s/<vcpu placement='static'>.*<\/vcpu>/<vcpu placement='static'>%s<\/vcpu>/g\" /data/vm_xml/s_centos.xml" % (vm_name,cpu,vm_name,ram,ram,cpu)
            res = run_command(alter_vm)
    	    pub = RedisHelper()
	    if res["exit_code"] == 0:
            	pub.publish("ok")
	    else:
		pub.publish("error")
	elif msg[2] == "ok" or msg[2] == "error":
            continue
	elif len(msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(",")) == 5:
	    vm_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(",")
	    if proform(vm_info) == "ok":
		pub = RedisHelper()
		pub.publish([msg[2],"ok"])
 	    else:
		pub = RedisHelper()
		pub.publish([msg[2],"failure"])
	elif len(msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(",")) == 2:
	    disk_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(",")
	    disk_name = disk_info[0].split("'")[1]
	    disk_size = disk_info[1].split("'")[1]
	    create_disk = "/vm_scripts/create_disk.sh %s %s" % (disk_name,disk_size)
	    run_command(create_disk)
	    pub = RedisHelper()
	    disk_result = [disk_name,disk_size,"ok"]
            pub.publish(disk_result)
	else:
  	    continue

