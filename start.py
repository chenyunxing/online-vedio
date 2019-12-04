from flask import Flask
from flask import render_template
import os
app = Flask(__name__,template_folder=os.path.join(os.getcwd(),'templates'))

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

def start(ip,port):
    print('----------------------------')
    print(os.getcwd())
    # ip,port = checkport()
    app.run(host='0.0.0.0',port=port,debug=False)




if __name__ == '__main__':
    # start()
    # 检查端口占用
    ip,port = checkport()
    app.run(host='0.0.0.0',port=port,debug=True)
    # main(['C:\\game','C:\\work\\redio\\downloadvideo-'])
    pass
