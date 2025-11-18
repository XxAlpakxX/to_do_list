from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from orm import ORM
class AddTaskWindow(QDialog):
    def __init__(self,selected_date, task_id):
        super().__init__()
        self.load_ui()
        self.orm = ORM('taskmanager')
        self.task_id = task_id
        self.task_name = self.orm.get_task_by_id(task_id)
        self.selected_date = selected_date
        self.setup_connections()
        if self.selected_date:
            self.window.selected_date.setText(f"Дата: {self.selected_date.toString('yyyy-MM-dd')}")
        if self.task_name:
            self.task_name = self.task_name[2]



    def load_ui(self):
        ui_file = QFile("add_task.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)    
        ui_file.close()
        layout = QVBoxLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
    def setup_connections(self):
        self.window.add_task_btn.clicked.connect(self.add_task)    

    def add_task(self):
        date = self.selected_date.toString("yyyy-MM-dd")
        start_time = self.window.start_time.time().toString() 
        duration = self.window.duration.time().toString() 
        remind_before = self.window.remind_before.time().toString() 
        description = self.window.description.toPlainText().strip()

        success = self.orm.update_task(self.task_id, self.task_name, date, start_time, duration, remind_before, description)
        if success:
            QMessageBox.information(self, "Успех", "Задача обновлена")
            self.accept()
            self.orm.set_status()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось обновить задачу")
    