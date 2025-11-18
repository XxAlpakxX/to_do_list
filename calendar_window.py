from PySide6.QtWidgets import *
from PySide6.QtCore import QFile, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate
from add_task_window import AddTaskWindow


class CalendarWindow(QDialog):
    date_selected = Signal(QDate)

    
    def __init__(self, user_id, task_id):
        super().__init__()
        self.load_ui()
        self.user_id = user_id
        self.task_id = task_id
        
        self.selected_date = None
        self.add_task_window = None
        
        

    def load_ui(self):
        ui_file = QFile("calendar_demo.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        layout = QGridLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
        
        self.setup_connections()

    def setup_connections(self):
        self.window.calendarWidget.clicked.connect(self.on_date_clicked)
        

    def on_date_clicked(self, date: QDate): 
        self.selected_date = date
        print(f"Выбранная дата: {self.selected_date.toString('yyyy-MM-dd')}")
        self.date_selected.emit(date)
        self.open_add_task_window()

    def get_selected_date(self):
        return self.selected_date
    
    def open_add_task_window(self):
        self.add_task_window = AddTaskWindow(self.selected_date, self.task_id)
        self.add_task_window.exec()    




    

        