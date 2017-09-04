from flask import Flask,render_template,request,redirect,make_response,session
from RedisHelper import RedisHelper
import threading,re
from time import ctime,sleep
from datetime import timedelta

app = Flask(__name__)
app.secret_key='lixin'

app.permanent_session_lifetime = timedelta(minutes=10)

msg = []

def pub(vm_info):
    pub = RedisHelper()
    pub.publish(vm_info)

def sub():
    sub = RedisHelper()
    redis_sub = sub.subscribe()
    while 1 < 2:
        global msg
        msg = redis_sub.parse_response()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username == "lixin" and password == "lixin") or (username == "jhk" and password == "jhk"):
            response = make_response(redirect('/index'))
            response.set_cookie('username', value=username, max_age=300)
            session['islogin'] = '1'
            return response
        else:
            session['islogin'] = '0'
            return "Your username or password failure."
    else:
        session['islogin'] = '0'
        return render_template('login.html')

@app.route('/index', methods=['GET','POST'])
def index():
    username = request.cookies.get('username')
    if not username:
        return "please login!!!"
    islogin = session.get('islogin')
    if request.method == 'POST':
        response = make_response(redirect('/vm_create'))
        response.set_cookie('username', value=username, max_age=300)
        session['islogin'] = '1'
        return response
    else:
        return render_template('index.html',username=username,islogin=islogin)

@app.route('/url')
def url():
    username = request.cookies.get('username')
    url = request.cookies.get('url')
    if not url:
        #url = 'Please Login.'
        return "please login!!!"
    islogin = session.get('islogin')
    return render_template('url.html',username=username, url=url, islogin=islogin)

@app.route('/vm_list', methods=['GET','POST'])
def vm_list():
    url = request.args.get('url')
    global vm_list
    global vm_info
    vm_list = []
    if url != None:
        response = make_response(redirect('/url'))
        response.set_cookie('url', value=url)
        return response
    else:
        if request.method == 'POST':
            vm_name = request.form.get('del_vm_name')
            username = request.cookies.get('username')
            delete = "delvm~" + vm_name
            pub(delete)
            sub = RedisHelper()
            redis_sub = sub.subscribe()
            while 1 < 2:
                msg = redis_sub.parse_response()
                if msg[2].split("~")[0] == "delvm":
                    continue
                else:
                    vm_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                    break
            for f in vm_info:
                list = f.split("'")[1].split("|")
                if len(list[1]) > 3:
                    port = "32"+list[1].split(".")[3]
                else:
                    port = "0"
                list.append(port)
                vm_list.append(list)

            if not username:
                return "please login!!!"
            islogin = session.get('islogin')
            return render_template('vm_list.html', username=username, islogin=islogin, vm_info=vm_list)
        else:
            username = request.cookies.get('username')
            pub("vm_list")
            sub = RedisHelper()
            redis_sub = sub.subscribe()
            while 1 < 2:
                msg = redis_sub.parse_response()
                if msg[2] == "vm_list":
                    continue
                else:
                    vm_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                    break
            for f in vm_info:
                list = f.split("'")[1].split("|")
                if len(list[1]) > 3:
                    port = "32" + list[1].split(".")[3]
                else:
                    port = "0"
                list.append(port)
                vm_list.append(list)

            if not username:
                return "please login!!!"
            islogin = session.get('islogin')
            return render_template('vm_list.html',username=username,islogin=islogin,vm_info=vm_list)

@app.route('/vm_detail', methods=['GET','POST'])
def vm_detail():
    username = request.cookies.get('username')
    vm_info = request.args.get('vm_name')
    vm_info = vm_info.split("[")[1].split("]")[0].split(",")
    if not username:
        return "please login!!!"
    islogin = session.get('islogin')
    if request.method == 'POST':
        cpu = request.form.get('cpu')
        ram = request.form.get('ram')
        if cpu == None and ram == None:
            oprate_vm = request.form.get('oprate_vm')
            oprate = oprate_vm.split("~")[0]
            if oprate == "start":
                pub(oprate_vm)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "start":
                        continue
                    else:
                        if msg[2] == "ok":
                            vm_info[3] = "running"
                        else:
                            return "error"
                        break
                return render_template('vm_detail.html', username=username, islogin=islogin, vm=vm_info)
            elif oprate == "shutdown":
                pub(oprate_vm)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "shutdown":
                        continue
                    else:
                        if msg[2] == "ok":
                            vm_info[3] = "shut_off"
                        else:
                            return "error"
                        break
                return render_template('vm_detail.html', username=username, islogin=islogin, vm=vm_info)
            elif oprate == "reboot":
                pub(oprate_vm)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "reboot":
                        continue
                    else:
                        if msg[2] == "ok":
                            vm_info[3] = "running"
                        else:
                            return "error"
                        break
                return render_template('vm_detail.html', username=username, islogin=islogin, vm=vm_info)
            else:
                pub(oprate_vm)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "reboot_force":
                        continue
                    else:
                        if msg[2] == "ok":
                            vm_info[3] = "running"
                        else:
                            return "error"
                        break
                return render_template('vm_detail.html', username=username, islogin=islogin, vm=vm_info)
        else:
            alter_name = request.form.get('alter_name')
            alter_args = "alter~"+alter_name+"~"+cpu+"~"+ram
            pub(alter_args)
            sub = RedisHelper()
            redis_sub = sub.subscribe()
            while 1 < 2:
                msg = redis_sub.parse_response()
                if msg[2].split("~")[0] == "alter":
                    continue
                else:
                    if msg[2] == "ok":
                        vm_info[1] = cpu
                        vm_info[2] = ram
                    else:
                        return "error"
                    break
            return render_template('vm_detail.html', username=username, islogin=islogin, vm=vm_info)
    else:
        return render_template('vm_detail.html',username=username,islogin=islogin,vm=vm_info)

@app.route('/vm_create', methods=['GET','POST'])
def vm_create():
    if request.method == 'POST':
        vm_name = request.form.get('vm_name')
        vm_cpu = request.form.get('vm_cpu')
        vm_memory = request.form.get('vm_memory')
        vm_disk = request.form.get('vm_disk')
        vm_images = request.form.get('vm_images')
        vm_info = [vm_name, vm_cpu, vm_memory, vm_disk, vm_images]

        threads = []
        t1 = threading.Thread(target=sub)
        threads.append(t1)
        t2 = threading.Thread(target=pub, args=(vm_info,))
        threads.append(t2)

        for t in threads:
            t.setDaemon(True)
            t.start()

        sleep(12)

        if len(msg) > 1 :
            print msg[2]
            info = msg[2].split("[")[2].split("]")[0].split(",|'")
            vm_name = info[0].split("'")[1]
            cpu = info[0].split("'")[3]
            mem = info[0].split("'")[5]
            disk = info[0].split("'")[7]
            os_type = info[0].split("'")[9]
            status = msg[2].split("]")[1].split("'")[1]
            vm_info = vm_name+","+cpu+","+mem+","+disk+","+os_type
            if status == "ok":
                response = make_response(redirect('/vm_list'))
                return response
            else:
                return "%s is created %s!" % (vm_info,status)
        else:
            session['islogin'] = '0'
            return "Your username or password failure."
    else:
        username = request.cookies.get('username')
        if not username:
            return "please login!!!"
        islogin = session.get('islogin')
        return render_template('vm_create.html', username=username, islogin=islogin)

@app.route('/disk_list', methods=['GET','POST'])
def disk_list():
    global disk_info
    disk_list = []
    if request.method == 'POST':
        disk_mount_umount = request.form.get('mount_umount')
        if disk_mount_umount != None:
            username = request.cookies.get('username')
            if disk_mount_umount.split("~")[0] == "umount":
                pub(disk_mount_umount)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "umount":
                        continue
                    else:
                        disk_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                        break
                for f in disk_info:
                    list = f.split("'")[1].split("|")
                    disk_list.append(list)

                if not username:
                    return "please login!!!"
                islogin = session.get('islogin')
                return render_template('disk_list.html', username=username, islogin=islogin, disk_info=disk_list)
            elif disk_mount_umount.split("~")[0] == "deldisk":
                disk_del = disk_mount_umount
                pub(disk_del)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "deldisk":
                        continue
                    else:
                        disk_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                        break
                for f in disk_info:
                    list = f.split("'")[1].split("|")
                    disk_list.append(list)

                if not username:
                    return "please login!!!"
                islogin = session.get('islogin')
                return render_template('disk_list.html', username=username, islogin=islogin, disk_info=disk_list)
            else:
                disk_name = request.form.get('mount_disk_name')
                disk_mount = disk_name + "~" + disk_mount_umount
                pub(disk_mount)
                sub = RedisHelper()
                redis_sub = sub.subscribe()
                while 1 < 2:
                    msg = redis_sub.parse_response()
                    if msg[2].split("~")[0] == "mount":
                        continue
                    else:
                        disk_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                        break
                for f in disk_info:
                    list = f.split("'")[1].split("|")
                    disk_list.append(list)

                if not username:
                    return "please login!!!"
                islogin = session.get('islogin')
                return render_template('disk_list.html', username=username, islogin=islogin, disk_info=disk_list)
        else:
            return "error."
    else:
        username = request.cookies.get('username')
        pub("disk_list")
        sub = RedisHelper()
        redis_sub = sub.subscribe()
        while 1 < 2:
            msg = redis_sub.parse_response()
            if msg[2] == "disk_list":
                continue
            else:
                disk_info = msg[2].split("[")[1].split("]")[0].split(",|'")[0].split(", ")
                break
        for f in disk_info:
            list = f.split("'")[1].split("|")
            disk_list.append(list)

        if not username:
            return "please login!!!"
        islogin = session.get('islogin')
        return render_template('disk_list.html', username=username, islogin=islogin, disk_info=disk_list)

@app.route('/disk_create', methods=['GET','POST'])
def disk_create():
    if request.method == 'POST':
        disk_name = request.form.get('disk_name')
        disk_size = request.form.get('disk_size')
        disk_info = [disk_name,disk_size]
        pub(disk_info)
        sub = RedisHelper()
        redis_sub = sub.subscribe()
        status = "failure"
        while 1 < 2:
            msg = redis_sub.parse_response()
            if len(msg[2].split("[")[1].split("]")[0].split(", ")) == 2:
                continue
            else:
                status = msg[2].split("]")[0].split(", ")[2].split("'")[1]
                break
        if status == "ok":
            response = make_response(redirect('/disk_list'))
            return response
        else:
            return "%s is created %s!" % (disk_name, status)
    else:
        username = request.cookies.get('username')
        if not username:
            return "please login!!!"
        islogin = session.get('islogin')
        return render_template('disk_create.html', username=username, islogin=islogin)

@app.route('/vm_migrate', methods=['GET','POST'])
def vm_migrate():
    if request.method == 'POST':
        vm_name = request.form.get('vm_name')
        KVM_IP = request.form.get('kvm_ip')
        migrate_info = "migrate~" + KVM_IP + "~" + vm_name
        pub(migrate_info)
        sub = RedisHelper()
        redis_sub = sub.subscribe()
        status = "failure"
        while 1 < 2:
            msg = redis_sub.parse_response()
            if msg[2].split("~")[0] == "migrate":
                continue
            else:
                status = msg[2]
                break
        if status == "ok":
            response = make_response(redirect('/migrate_results'))
            result = vm_name + "~" + status
            response.set_cookie('result', value=result)
            return response
        else:
            response = make_response(redirect('/migrate_results'))
            result = vm_name + "~" + status
            response.set_cookie('result', value=result)
            return response
    else:
        username = request.cookies.get('username')
        if not username:
            return "please login!!!"
        islogin = session.get('islogin')
        return render_template('vm_migrate.html',username=username,islogin=islogin)

@app.route('/migrate_results')
def migrate_results():
    username = request.cookies.get('username')
    result = request.cookies.get('result')
    if not username:
        return "please login!!!"
    islogin = session.get('islogin')
    return render_template('migrate_results.html', username=username, result=result, islogin=islogin)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)
