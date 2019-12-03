# coding=utf-8
# 主窗口类
import PySimpleGUI as sg
import start
import threading
import _thread

import ctypes

sg.change_look_and_feel('DarkAmber')    # 背景风格设置
# 主题窗口架构
layout = [  [sg.Text('请选择你要部署的文件夹')],
            [sg.Text('选择或者输入文件夹路径'), sg.InputText(key='fold_temp'),sg.Button('浏览',key='get_fold'),sg.Button('添加',key='add')], # 输入框
            [sg.Listbox(key='fold_text',values=[],size=(35, 15))],
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
        if not node:
            node = threading.Thread(target=start.start,args=(dir_list))
            node.setDaemon(True)
            node.start()
            print('start')
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
