# IaaS_admin
This is a small IaaS platform management system based on Flask.
================================================================================================
详细内容见博客：https://www.cnblogs.com/wsjhk/p/7638269.html
虚拟化管理系统

前言
    kvm虚拟化平台的介绍，结合国内外云计算技术发展说明设计虚拟化管理系统的优点和必要性。

第一章 kvm虚拟化原理
    介绍kvm虚拟化原理

第二章 虚拟化平台的搭建操作
    搭建kvm虚拟化平台的过程，包括安装操作系统，kvm，配置kvm，命令的基本使用和创建虚拟机

第三章 虚拟机镜像的制作(shellinbox,novnc,guacamole)
    根据需要创建虚拟机，在虚拟机上安装好需要用到的各种软件，并将其作为基础镜像配置保存下来。

第四章 虚拟机动态迁移
    实现虚拟机的动态迁移过程

第五章 虚拟化管理系统的设计
    介绍虚拟化管理系统设计原理和功能结构，界面的设计，实现的功能有：创建虚拟机，删除虚拟机，修改虚拟机配置参数，虚拟机动态迁移，重启虚拟机，虚拟机关机启动，添加磁盘，vnc远程操作虚拟机。

第六章 虚拟化管理系统的实现
    实现虚拟化管理系统的过程和功能演示  

================================================================================================
虚拟化管理系统完成有待优化问题和处理的bug如下：

问题一：执行时偶尔会出现以下不需要执行的命令，导致执行时间过长，需要优化：
vm_list
['centos|192.168.0.118|1|2048000|centos|running', 'winxp_01|192.168.0.106|1|204800|winxp|running']
/bin/sh: 192.168.0.118: command not found
/bin/sh: 192.168.0.106: command not found
/bin/sh: 2048000: command not found
/bin/sh: running_winxp_01: command not found
/bin/sh: centos: command not found
/bin/sh: 1: command not found
/bin/sh: 1: command not found
/bin/sh: running: command not found
/bin/sh: 1: command not found
/bin/sh: winxp: command not found
/bin/sh: running: command not found
/bin/sh: 192.168.0.106: command not found
/bin/sh: 204800: command not found
/bin/sh: 204800: command not found
/bin/sh: winxp: command not found
['centos|192.168.0.118|1|2048000|centos|running_winxp_01|192.168.0.106|1|204800|winxp|running', 'winxp_01|192.168.0.106|1|204800|winxp|running', 'ok']

问题二：功能代码需要写成函数进行封装，减少代码量。优化代码。

问题三：session共享和超时的问题。

问题四：判断虚拟机操作系统类型还没有真正实现，需要优化。

================================================================================================
原理图简单如下：

-------------        --------------------         ----------------------------       ----------
-- Web_kvm -- <----> -- redis(sub/pub) -- <-----> -- vm_scripts(python_kvm) -- ----> -- *.sh --
-------------        --------------------         ----------------------------       ----------

===============================================================================================
