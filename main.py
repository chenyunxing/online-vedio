# coding=utf-8
# 主窗口类
import PySimpleGUI as sg
import start
import threading
import _thread
import os
import socket
import ctypes

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
    path = os.path.abspath(path)
    for i in os.listdir(path):
        os.remove(os.path.join(path,i))
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
        if(dir_path!='.' and dir_path!='..' and os.path.isdir(dir_path)):
            temp = os.path.abspath(dir_path)
            (_, temp) = os.path.split(temp)
            soft_dir_list.append(pre + '-' + str(flag)+ '-' + temp)
            flag = flag + 1
        else:
            print(dir_path)
            return False
    # 到此处目录都存在，开始建立软连接
    setLink(soft_dir_list, dir_path_list)
    return True

sg.change_look_and_feel('DarkAmber')    # 背景风格设置
# 主题窗口架构
layout = [  [sg.Text('请选择你要部署的文件夹')],
            [sg.Text('选择或者输入文件夹路径'), sg.InputText(key='fold_temp'),sg.Button('浏览',key='get_fold'),sg.Button('添加',key='add')], # 输入框
            [sg.Listbox(key='fold_text',values=[],size=(35, 15))],
            [sg.Text('未开启',key='tip', size=(35,1))],
            [sg.Button('开始',key='start'), sg.Button('Cancel')] ]
# 创建窗口
window = sg.Window('Window Title', layout, default_element_size=(40, 20))
# sg.PopupGetFolder('Please enter a folder name',no_window=True)
# Event Loop to process "events" and get the "values" of the inputs
# 定义已获取的文件夹列表
dir_list = []
# 存储线程的节点
node = ''
while True:
    event, values = window.read()
    # print(event)
    if event == 'get_fold':
        text = sg.PopupGetFolder('Please enter a folder name',no_window=True)
        window['fold_temp'].update(text)
    if event == 'add':
        if values['fold_temp'] not in dir_list:
            dir_list.append(values['fold_temp'])
            window['fold_text'].update(dir_list)
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        # if node:
        #     stop_thread(node)
        break
    if event == 'start':
        if not main(dir_list):
            print('error')
        if not node:
            print(type(dir_list))
            ip,port = checkport()
            node = threading.Thread(target=start.start,args=(ip,port))
            node.setDaemon(True)
            node.start()
            print('start')
            tip_str = '已开启,网址为:'+ ip + ':' + str(port)
            window['tip'].update(tip_str)
    # print('You entered ', values[0])
# sg.Listbox(values=('1990年','1991年','1992年'), size=(30, 5))],
window.close()
# sg.Popup('title?!', 'This is the shortest GUI program ever!') # 弹窗

# event, values = sg.Window('Get filename example', [[sg.Text('Filename')], [sg.Input(), sg.FileBrowse()], [sg.OK(), sg.Cancel()] ]).Read() # 文件选择框，不可文件夹
# print(values)

# 优雅格式后的文件选择框
# import PySimpleGUI as sg

# layout = [[sg.Text('Filename')],
#           [sg.Input(), sg.FileBrowse()],
# 	  [sg.OK(), sg.Cancel()]]

# window = sg.Window('Get filename example', layout)

# event, values = window.Read()

# sg.Popup('title?!', 'This is the shortest GUI program ever!')
# text = sg.PopupGetFolder('Please enter a folder name')
# text = sg.PopupGetFolder('Please enter a folder name',no_window=True)  # 加上nowindow，可以直接弹窗选择文件夹，没有确定等操作
# sg.Popup('Results', 'The value returned from PopupGetFolder', text)
