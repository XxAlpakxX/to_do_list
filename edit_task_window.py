from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate, QTime
from orm import ORM
class EditTaskWindow(QDialog):
    def __init__(self, task_id):
        super().__init__()
        self.orm = ORM('taskmanager')
        self.load_ui()
        self.task_id = task_id
        #selected_date = self.orm.get_date(task_id)
        self.load_data()

    def load_ui(self):
        ui_file = QFile("EditTaskWindow.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        layout = QVBoxLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
        
        self.setup_connections()
 

    def setup_connections(self):    
        self.window.edit_info_btn.clicked.connect(self.get_new_info)

    def load_data(self): 
        task_data = self.orm.get_task_by_id(self.task_id)
        if task_data:
            task_name  = task_data[2] or ""
            date_str = task_data[4]
            start_time_str = task_data[5]
            duration_str = task_data[6]
            remind_before_str = task_data[7]
            description = task_data[3] or ""

            self.window.task_name.setText(task_name)
            self.window.description.setPlainText(description)


           
            if date_str:
                self.window.date.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
            
            self.window.start_time.setTime(QTime.fromString(start_time_str, "hh:mm:ss"))
            self.window.duration.setTime(QTime.fromString(duration_str, "hh:mm:ss"))
            self.window.remind_before.setTime(QTime.fromString(remind_before_str, "hh:mm:ss"))
            
            self.window.description.setPlainText(description)
        else:
            QMessageBox.warning(self, "Ошибка", "Задача не найдена")
        
    def get_new_info(self):
        task_name  = self.window.task_name.text().strip()
        date = self.window.date.date().toString("yyyy-MM-dd")
        start_time = self.window.start_time.time().toString() 
        duration = self.window.duration.time().toString() 
        remind_before = self.window.remind_before.time().toString() 
        description = self.window.description.toPlainText().strip()
        success = self.orm.update_task(self.task_id, task_name, date, start_time, duration, remind_before, description)
        if success:
            QMessageBox.information(self, "Успех", "Задача изменена")
            self.load_data()
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить задачу")



