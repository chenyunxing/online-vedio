from flask import Flask
from flask import render_template
import os
import socket
app = Flask(__name__)

# dir = 'C:\\Users\\yinxixing'
dir = './static/'
# dir = 'C:\\game'
@app.route('/')
def hello_world():
    infos = os.listdir(dir)
    # 遍历static目录下的文件夹
    data = []
    name = []
    for info in infos:
        fold_path = os.path.join(dir,info)
        # 如果是一个目录，则在前端遍历输出目录下的.mp4文件
        if info != '.' and info != '..' and os.path.isdir(fold_path):
            name.append(info)
            temp = []
            for i in os.listdir(fold_path):
                if '.mp4' in i:
                    temp.append(i)
            data.append(temp)
    return render_template('mp4.html', zipdata=zip(name,data))

@app.route('/test/<dirname>/<name>')
def test(dirname=None,name=None):
    # dirname = 'game'
    return render_template('hello.html', name=name,dirname=dirname)

# 检查端口找到可用端口开启服务
def checkport():
    ip = '127.0.0.1'
    port = 8080
    socket.setdefaulttimeout(1)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=s.connect_ex((ip, port))
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    ip = myaddr
    if result == 0:
        while result==0:
            port = port + 1
            print(port)
            result=s.connect_ex((ip, port))
            if port == 60000:
                print('too many port used')
                return -1
    return ip,port

# 建立软连接
def setLink(nameList,pathList):
    return_dir_list = [] # 返回的目录列表
    # 首先清空static文件夹
    path = './static'
    os.removedirs(path)
    # 重新建立static文件夹
    os.mkdir(path)
    # 获取绝对路径
    abspath = os.path.abspath(path)
    # 建立软连接
    for dst,path in zip(nameList,pathList):
        temp = os.path.join(abspath,dst)
        path = os.path.abspath(path) # 顺手获取绝对路径，用绝对路径建立软连接，虽然感觉没有应该也没关系
        os.symlink(path, temp)
        return_dir_list.append(temp)
    return return_dir_list

# 定义主函数，传入参数为文件夹路径列表
def main(dir_path_list):
    pre = 'video' # 软连接前缀
    soft_dir_list = [] # 文件夹连接名字的列表
    flag = 0 # 计数器，避免同名情况
    # 第一步判断是否每个路径都是文件夹，如果有一个不是，则返回错误
    for dir_path in dir_path_list:
        if(os.path.isdir(dir_path)):
            temp = os.path.abspath(dir_path)
            (_, temp) = os.path.split(temp)
            soft_dir_list.append(pre + '-' + str(flag)+ '-' + temp)
            flag = flag + 1
        else:
            return False
    # 到此处目录都存在，开始建立软连接
    video_list = setLink(soft_dir_list, dir_path_list)
    # 获取视频列表成功，随后开始编写模板

def start(dir_path_list):
    print('----------------------------')
    main(dir_path_list)
    ip,port = checkport()
    app.run(host='0.0.0.0',port=port,debug=False)
    return 'succe'




if __name__ == '__main__':
    # start()
    # 检查端口占用
    ip,port = checkport()
    app.run(host='0.0.0.0',port=port,debug=True)
    # main(['C:\\game','C:\\work\\redio\\downloadvideo-'])
    pass
