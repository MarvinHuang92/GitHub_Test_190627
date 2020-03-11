import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtGui import QPalette,QBrush,QPixmap

global path

#定义读取之前三个py文件的函数
def CreatText():
    os.system("python Get_dwg_filename.py")
def Find_UnExist_Number():
    os.system("python Find_UnExist_Number.py")
def Information_Fill():
    os.system("python Information_Fill.py")

#绘制UI的Class
class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()

        #设定主界面尺寸
        self.resize(300,350)
        self.title="Auto Fill Information"

        #插入背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('nexteer2.png')))
        self.setPalette(palette1)


        #生成控件实体
        self.setWindowTitle(self.title)#标题
        self.textbox = QLineEdit(self)#路径文本框
        self.textbox2 = QLineEdit(self)  # 日期文本框
        self.button = QPushButton('1.检查图纸完整性', self)
        self.button2 = QPushButton('2.填充信息', self)
        self.textEdit = QTextEdit(self)#反馈文本框
        self.textEdit2 = QTextEdit(self) #结果文本框
        self.label1=QLabel('文件路径', self)
        self.label2=QLabel('缺失图纸', self)
        self.label3 = QLabel('填表日期', self)
        self.label4=QLabel('运行结果', self)

        #调整框体位置和大小
        self.textbox.resize(230,20) #路径文本框
        self.textbox2.resize(230, 20) #日期文本框
        self.textEdit.resize(230,55) #缺失图纸文本框
        self.textEdit2.resize(230, 70)  #结果文本框
        self.button.resize(120,40)
        self.button2.resize(90,40)


        self.textEdit.move(60,60) #缺失图纸文本框
        self.textEdit2.move(60, 120)  #结果文本框
        self.textbox.move(60, 5)  # 路径文本框
        self.textbox2.move(60, 30) #日期文本框
        self.label1.move(6,8) #文件路径
        self.label2.move(6,80) #缺失图纸
        self.label3.move(6,35) #填表日期
        self.label4.move(6,150) #运行结果

        self.button.move(58,205)  #按钮1
        self.button2.move(200,205) #按钮2

        #Layout布局
        '''
        self.v_layout=QVBoxLayout()
        self.v_layout.addWidget(self.label1)
        self.v_layout.addWidget(self.label2)
        self.v_layout.addWidget(self.textEdit)
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.button2)
        '''

        #定义按钮与槽函数的连接方式
        self.button.clicked.connect(self.Get_Path)
        self.button.clicked.connect(self.Find_UnExist)
        self.button.released.connect(self.Get_Date)
        self.button2.clicked.connect(self.Information)

    #槽函数（按下按钮后干什么事）
    def Get_Path(self):
        global textboxValue
        textboxValue = self.textbox.text()
        f = open("path.txt", 'w')
        f.write(textboxValue)
        f.close()
    def Get_Date(self):
        global textboxValue2
        textboxValue2 = self.textbox2.text()
        f = open("date.txt", 'w')
        f.write(textboxValue2)
        f.close()

    def Find_UnExist(self):
        CreatText()
        time.sleep(0.1)
        Find_UnExist_Number()
        time.sleep(0.1)
        file = open('UnExist.txt')
        file_path = file.read()
        self.textEdit.setPlainText('缺失图表编号为：'+file_path)
    def Information(self):
        Information_Fill()
        file = open('log.txt')
        file_path = file.read()
        self.textEdit2.setPlainText(file_path)

#不知道什么东西的东西
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()  # 6
    demo.show()  # 7
    sys.exit(app.exec_())
