from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets
from data_visualize import data_

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('ui_files/mainwindow.ui', self)
        
        global data, steps
        data = data_()
        
        self.Browse = self.findChild(QPushButton, "Browse") # findChild는 내가 쓰고 싶은 버튼을 찾아주는 함수
        self.columns = self.findChild(QListWidget, "Column_list")
        
        self.Browse.clicked.connect(self.get_csv) ## Browse를 클릭했을 때 실행되게 만드는 함수 clicked.connect()
        
        
        # self.show() 
    def filldetails(self, fleg = 1):
        if fleg  == 0 :
            self.df = data.read_file(str(self.file_path))
        
        self.columns.clear() # columns 안에 있는 내용들을 지워버리는 함수
        self.column_list = data.get_column_list(self.df)
        # print(self.column_list)    
        
        for i , j in enumerate(self.column_list): ## enumerate() 함수는 인덱스까지 뽑게 만들어 줄 수 있음.
            stri = f'{j}------{str(self.df[j].dtype)}' ##j는 리스트 이름, 데이터 타입 보기
            print(stri)
            self.columns.insertItem(i, stri) ##i는 순서를 나타냄 QListWidget 에 값을 넣어주고 싶을 때 사용하는 함수 insertItem()

            
    
    def get_csv(self):
        self.file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "csv(*.csv)")
        self.columns.clear()
        
        if self.file_path != "":
            self.filldetails(0)
        
        
if __name__ == '__main__' :
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()
    
    sys.exit(app.exec_())