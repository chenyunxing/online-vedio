from flask import Flask
from flask import render_template
import os
app = Flask(__name__)

# dir = 'C:\\Users\\yinxixing'
dir = 'C:\\game'
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
    dirname = 'game'
    return render_template('hello.html', name=name,dirname=dirname)

if __name__ == '__main__':
    # 检查端口占用
    import socket
    ip = '127.0.0.1'
    port = 8080
    socket.setdefaulttimeout(3)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result=s.connect_ex((ip, port))
    if result==0:
        print(str(ip,u':',str(port),u'端口已占用')
    app.run(host='0.0.0.0', port=8080,debug=True)
