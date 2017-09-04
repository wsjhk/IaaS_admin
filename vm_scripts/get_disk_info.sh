#!/bin/bash 

printf "磁盘名称|磁盘大小|状态\n"
if [[ `cat /vm_scripts/disk_list` == "" || `cat /vm_scripts/disk_list` == "#|#|#" ]];then
    echo "#|#|#" > /vm_scripts/disk_list
else
    sed -i "/#|#|#/"d /vm_scripts/disk_list
fi

all=`grep -vE "^$" /vm_scripts/disk_list|wc -l`
unuse=`grep "unuse" /vm_scripts/disk_list|grep -vE "^$"|wc -l`
used=`expr $all - $unuse`

cat /vm_scripts/disk_list

echo -ne "\n一共有$all个磁盘,$used个磁盘在使用,$unuse个磁盘未使用.\n"
