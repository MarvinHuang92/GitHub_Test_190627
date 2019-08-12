# -*- coding:UTF-8 -*-

import os
# python3 是小写 tkinter
from tkinter import *
# 导入ttk
from tkinter import ttk, dialog, filedialog

customer_file_path = 'config/custom'
save_file_path = 'config/bin'

class App:
    def __init__(self, master):
        self.master = master
        self.initWidgets()
    def initWidgets(self):
        self.strVar0 = StringVar()                  # desktop
        self.strVar1 = StringVar()                  # CANape
        self.strVar2 = StringVar()                  # CANalyzer (file, not dir)
        self.strVar3 = StringVar()                  # executables
        self.strVar4 = StringVar()                  # PR_Build_Artifacts

        self.intVar0 = IntVar()                     # Flash Time Limit
        self.intVar1 = IntVar()                     # CANalyzer Trace Time

        LSD = Frame(self.master)                    # 设置容器，Load Save Default
        LSD.pack(side=TOP, pady=10)                 # Y方向留空10像素

        label_text = ['Desktop:', 'CANape path:', 'CANalyzer path:', 'Executables path:', 'PR Build Artifacts:']
        lb = []
        for i in range(5):
            lb.append(Label(LSD, text=label_text[i], width=14, height=1, anchor=W, font=("Arial", 9)))
            lb[i].grid(row=i, column=0, padx=8, pady=3)

        # 创建Combobox组件,并绑定到self.strVar0变量
        self.cb0 = ttk.Combobox(LSD, width=70, height=1, font=("Arial", 9), textvariable=self.strVar0)
            # postcommand=self.choose)                # 当用户单击下拉箭头时触发self.choose方法
        self.cb0.grid(row=0, column=1, columnspan=2, padx=8)
        self.cb0['values'] = ['Python', 'Ruby', 'Kotlin', 'Swift']

        self.cb1 = ttk.Combobox(LSD, width=70, height=1, font=("Arial", 9), textvariable=self.strVar1)
        self.cb1.grid(row=1, column=1, columnspan=2, padx=8)
        self.cb1['values'] = ['Python2', 'Ruby2', 'Kotlin2', 'Swift2']

        self.bt04 = Button(LSD, text='Choose...', width=7, height=1, font=("Arial", 9))  # command=self.open_file)
        self.bt04.grid(row=0, column=4, padx=3)

        self.bt04 = Button(LSD, text='Reset', width=7, height=1, font=("Arial", 9))  # command=self.open_file)
        self.bt04.grid(row=0, column=5, padx=3)

        p2 = Frame(self.master)                     # 设置pack2容器
        p2.pack(side=TOP, pady=10)

        self.label1 = Label(p2, text="目标路径:")
        self.label1.grid(row=0, column=0)
        # self.label1.pack(side=TOP)

        # self.entry1 = Entry(p2, textvariable=self.path)
        # self.entry1.grid(row=0, column=1)
        # self.entry1.pack(side=TOP)

        self.button1 = Button(p2, text="路径选择", command=self.selectPath)
        self.button1.grid(row=0, column=2)
        # self.button1.pack(side=TOP)
        
        f = Frame(self.master)                      # 第三个容器
        f.pack()
        self.isreadonly = IntVar()
        # 创建Checkbutton，绑定到self.isreadonly变量
        Checkbutton(f, text = '是否只读:',
            variable=self.isreadonly,
            command=self.change).pack(side=LEFT)
        # 创建Button，单击该按钮激发setvalue方法
        Button(f, text = 'Reset Config',
            command=self.setvalue).pack(side=RIGHT)

        f2 = Frame(self.master)                      # 第四个容器
        f2.pack()

        self.text1 = Text(f2, width=50, height=10)
        self.text1.pack(side=TOP)

        # self.bt1 = Button(f2, text='打开文件', width=15, height=2, command=self.open_file)
        # self.bt1.pack()
        # self.bt2 = Button(f2, text='保存文件', width=15, height=2, command=self.save_file)
        # self.bt2.pack()

    def open_file(self):
        global file_path
        global file_text
        file_path = filedialog.askopenfilename(title=u'选择文件',
            initialdir=(os.path.expanduser('C:/')))  # 设置默认路径
        print('打开文件：', file_path)
        if file_path is not None:
            with open(file=file_path, mode='r+', encoding='utf-8') as file:
                file_text = file.read()
            self.text1.insert('insert', file_text)

    def save_file(self):
        global file_path
        global file_text
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        print('保存文件：', file_path)
        file_text = self.text1.get('1.0', END)
        if file_path is not None:
            with open(file=file_path, mode='a+', encoding='utf-8') as file:
                file.write(file_text)
            self.text1.delete('1.0', END)
            dialog.Dialog(None, {'title': 'File Modified', 'text': '保存完成', 'bitmap': 'warning', 'default': 0,
                                 'strings': ('OK', 'Cancel')})
            print('保存完成')

    # get（）方法获取内容：
    # txt = entry.get()
    # txt2 = text.get('0.0', END)
    # 第一个参数‘0.0’是指从第0行第0列开始读取，第二个参数END表示最后一个字符(实际上是tkinter.END，必须全大写)

    def choose(self):
        pass
        # from tkinter import messagebox
        # 获取Combbox的当前值
        # messagebox.showinfo(title=None, message=str(self.cb1.get()))
    def change(self):
        self.cb1['state'] = 'readonly' if self.isreadonly.get() else 'enable'
    def setvalue(self):
        self.strVar1.set('我爱Python')

    def selectPath(self):
        self.path_ = filedialog.askdirectory()
        self.path.set(self.path_)




root = Tk()                                     # 创建Tk对象，Tk代表窗口
root.title('Auto Smoke Test Config')            # 设置窗口标题

w = 800
h = 600

# 定义函数：令窗口居中
def center_window(w = 300, h = 200):
    ws = root.winfo_screenwidth()	            # 读取显示器分辨率
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)			   	            # x,y是窗口左上角坐标
    y = (hs/2) - (h/2)
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    root.resizable(False, False)                # 禁止窗口缩放（第一个宽，第二个高）

center_window(w, h)                             # 调用自定义函数令窗口居中

# 改变窗口图标
# root.iconbitmap('images/fklogo.ico')
App(root)
root.mainloop()
