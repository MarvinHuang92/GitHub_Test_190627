import sys
import PyQt5
import pyautocad
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from pyautocad import Autocad

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        #设定UI尺寸
        self.setMaximumSize(380, 60)
        self.setMinimumSize(380, 60)
        self.title="PyAutoDim"

        #插入背景图片
        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('Nexteer_Button.png')))
        self.setPalette(palette1)

        #生成控件实体
        self.setWindowTitle(self.title)
        self.button = QPushButton('Change the DimColor', self)

        #调整框体位置和大小
        self.button.resize(180, 50)
        self.button.move(180, 3)

        #槽函数
        self.button.clicked.connect(self.Auto_Mark)


    def Auto_Mark(self):
        # 连接CAD
        acad = Autocad(create_if_not_exists=True)

        # 设定变量
        for leader in acad.iter_objects('Leader'):
            leader.DimensionLineColor = 2

        for dim in acad.iter_objects('Dimension'):
            attribute = dir(dim)
            dim.TextColor = 2
            dim.DimensionLineColor = 2
            dim.ExtensionLineColor = 2

while True:
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
