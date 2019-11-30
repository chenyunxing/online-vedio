from flask import Flask
from flask import render_template
import os
import socket
app = Flask(__name__)

dir = 'C:\\Users\\yinxixing'
# dir = 'C:\\game'
@app.route('/')
def hello_world():
    infos = os.listdir(dir)
    list_mp4 = []
    for info in infos:
        if '.mp4' in info:
            temp = '<a href="test/' + info +'">' + info + '</a>'
            list_mp4.append(temp)
    return '<br>'.join(list_mp4)

@app.route('/test/<name>')
def test(name=None,dirname='videos'):
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
def setLink(pathList):
    # 首先清空static文件夹
    path = './static'
    os.removedirs(path)
    # 重新建立static文件夹
    os.mkdir(path)
    video_num = 0
    # 建立软连接
    for path in pathList:
        dst = './static/video' + str(video_num)
        video_num = video_num + 1
        os.symlink(path, dst)
    # 把video的数量记录下来，晚点用于前端展示

if __name__ == '__main__':
    # 检查端口占用
    ip,port = checkport()
    app.run(host='0.0.0.0',port=port,debug=True)
