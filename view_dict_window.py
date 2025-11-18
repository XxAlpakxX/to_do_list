from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from orm import ORM
class ViewDictWindow(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.load_ui()
        self.user_id = user_id
        self.orm = ORM('taskmanager')  
        self.load_data_detalied()
        self.resize(800, 600)
       

    def load_ui(self):
        ui_file = QFile("ViewTasks.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        layout = QVBoxLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
        self.setup_connections()

    def setup_connections(self):
        self.window.back_btn.clicked.connect(self.close)
    
   
    def load_data_detalied(self):
        
        rows = self.orm.get_data_detalied(self.user_id)
        
        table_widget = self.window.tableWidget
        table_widget.setRowCount(len(rows))
        table_widget.setColumnCount(7)  
        
        headers = ["Задача", "Дата", "Начало", "Длительность", "Напомнить за", "Описание", "Статус"]
        table_widget.setHorizontalHeaderLabels(headers)

        
        colors = {
            "Просрочена": QColor(255, 182, 193),     # Светло-розовый
            "В процессе": QColor(255, 255, 180),     # Светло-жёлтый
            "Запланирована": QColor(200, 250, 200),  # Светло-зелёный
            "Завершена": QColor(200, 200, 255),      # Светло-синий 
            "Ошибка": QColor(255, 200, 200)          # Серо-розовый
        }

     
        for row_idx, row_data in enumerate(rows):
            task_name, description, date, start_time, duration, remind_before,  status = row_data

          
            row_items = [
                task_name,
                date or "",
                start_time or "",
                duration or "",
                remind_before or "",
                description or "",
                status or "Неизвестно"
            ]

            for col_idx, value in enumerate(row_items):
                item = QTableWidgetItem(str(value))
               
                if col_idx == 6 and str(value) in colors:
                    item.setBackground(colors[str(value)])
                table_widget.setItem(row_idx, col_idx, item)

        
        table_widget.resizeColumnsToContents()           
        table_widget.horizontalHeader().setStretchLastSection(True)             