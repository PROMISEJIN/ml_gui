from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets
from data_visualize import data_
from table_display import DataFrameModel

class UI(QMainWindow):
    
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('ui_files/mainwindow.ui', self)
        
        global data, steps
        data = data_()
        
        self.Browse = self.findChild(QPushButton, "Browse") # findChild는 내가 쓰고 싶은 버튼을 찾아주는 함수
        self.columns = self.findChild(QListWidget, "Column_list")
        self.table= self.findChild(QTableView, "tableView")
        self.data_shape= self.findChild(QLabel, "Shape")
        self.Submit= self.findChild(QPushButton, "Submit") # target 컬럼 결정버튼 호출
        self.target_name= self.findChild(QLabel, "target_name") # target 컬럼 보는 창 호출
        self.dropcolumn= self.findChild(QComboBox, "dropcolumn") # target 컬럼 결정하는 박스 호출
        self.drop= self.findChild(QPushButton, "drop") #target 컬럼 삭제하는 버튼 호출
        
        self.Scaler= self.findChild(QComboBox, "Scaler") # Scale 하는 함수 호출 
        self.Scale_btn= self.findChild(QPushButton, "Scale_btn") # Scale 오른쪽 버튼
        
        
        
        self.Browse.clicked.connect(self.get_csv) ## Browse를 클릭했을 때 실행되게 만드는 함수 clicked.connect()
        self.columns.clicked.connect(self.target)
        self.Submit.clicked.connect(self.set_target)
        self.drop.clicked.connect(self.dropc)
        
        self.Scale_btn.clicked.connect(self.scale_value)
        
        
        
        
        # self.show() 
    def filldetails(self, fleg = 1):
        if fleg  == 0 :
            self.df = data.read_file(str(self.file_path))
        
        self.columns.clear() # columns 안에 있는 내용들을 지워버리는 함수
        self.column_list = data.get_column_list(self.df)
        # print(self.column_list)    
        
        for i , j in enumerate(self.column_list): ## enumerate() 함수는 인덱스까지 뽑게 만들어 줄 수 있음.
            stri = f'{j} ------ {str(self.df[j].dtype)}' ##j는 리스트 이름, 데이터 타입 보기
            print(stri)
            self.columns.insertItem(i, stri) ##i는 순서를 나타냄 QListWidget 에 값을 넣어주고 싶을 때 사용하는 함수 insertItem()
            
        x, y = self.df.shape
        self.data_shape.setText(f'({x} , {y})')
        self.fill_combo_box()
        
    def target(self):
        self.item = self.columns.currentItem().text().split(' ')[0]
        print(self.columns.currentItem().text().split(' ')[0])
        
    def set_target(self):
        self.target_value = self.item
        self.target_name.setText(self.target_value)
    
    def dropc(self):
        selected = self.dropcolumn.currentText()
        self.df = data.drop_columns(self.df , selected)
        self.filldetails()
    
    def scale_value(self):
        if self.Scaler.currentText() == 'StandardScale':
            self.df = data.StandardScale(self.df, self.target_value)
            
        elif self.Scaler.currentText() == 'MinMaxScaler':
            self.df = data.MinMaxScale(self.df, self.target_value)
        
        else :
            self.df = data.PowerScale(self.df, self.target_value)
            
        self.filldetails()
        
    def fill_combo_box(self):
        self.dropcolumn.clear()
        self.dropcolumn.addItems(self.column_list)
        x = DataFrameModel(self.df)
        self.table.setModel(x)
        
        

            
    
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