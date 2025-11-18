from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QTimer
from orm import ORM
from calendar_window import CalendarWindow
from view_dict_window import ViewDictWindow
from edit_task_window import EditTaskWindow


class MainWindow(QMainWindow):
    
    def __init__(self, user_id, login_window_ref = None):
        super().__init__()

        self.load_ui()
  
        self.user_id = user_id
        self.calendar_window = None
        self.orm = ORM('taskmanager')
        self.current_task_id = None
        self.view_tasks_window = None
        self.edit_task_window = None
        self.login_window_ref = login_window_ref 
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_statuses_periodically)
        self.status_timer.start(60000)  

        self.load_data()

    def load_ui(self):
        ui_file = QFile("TMMainWindow.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        layout = QGridLayout()
        layout.addWidget(self.window)
        self.setLayout(layout)
        self.setCentralWidget(self.window)
        self.setup_connections()
        self.setup_contextmenu()

    def setup_connections(self):
        self.window.add_task_btn.clicked.connect(self.add_task)
        self.window.show_tasks_btn.clicked.connect(self.open_view_tasks_window)    
        self.window.back_btn.clicked.connect(self.logout)

    def setup_contextmenu(self):
        self.window.task_viewer_demo.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.task_viewer_demo.customContextMenuRequested.connect(self.show_contextmenu)
        
    
    def logout(self):
        """Выход из системы и возврат к окну входа"""
        reply = QMessageBox.question(
            self,
            "Подтверждение выхода",
            "Вы уверены, что хотите выйти?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.status_timer.isActive():
                self.status_timer.stop()
                
            if self.calendar_window:
                self.calendar_window.close()
            if self.view_tasks_window:
                self.view_tasks_window.close()
            if self.edit_task_window:
                self.edit_task_window.close()
                
            
            if self.login_window_ref:
                self.login_window_ref.show()
            self.close()

    def add_task(self):
        task_name = self.window.task_input.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return None
        success = self.orm.insert_task(self.user_id, task_name)  
        if success:
            QMessageBox.information(self, "Успех", "Задача добавлена")
            self.window.task_input.clear()
            self.current_task_id = success
            self.load_data()
            self.open_calendar()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось добавить задачу")


    def load_data(self): 
        rows = self.orm.get_data(self.user_id)
        print(f"Loaded {len(rows)} tasks for user {self.user_id}")
        table_widget = self.window.task_viewer_demo
        table_widget.setRowCount(len(rows))
        table_widget.setColumnCount(1)  
        table_widget.setHorizontalHeaderLabels(["Название задачи"])

        for row_idx, row_data in enumerate(rows):
            item = QTableWidgetItem(str(row_data[0]))  
            table_widget.setItem(row_idx, 0, item)

    def update_statuses_periodically(self):
        self.orm.set_status()
        if self.view_tasks_window and self.view_tasks_window.isVisible():
            self.view_tasks_window.load_data_detalied()
        self.load_data()        
        
    
    def show_contextmenu(self, position):
        index = self.window.task_viewer_demo.indexAt(position)
        if not index.isValid():
            return
        
        item = self.window.task_viewer_demo.item(index.row(), 0)
        if item is None:
            return
        task_name = item.text()
        task_id = self.orm.get_task_id_by_name(self.user_id, task_name)

        menu = QMenu(self)
        edit_action = menu.addAction("Редактировать")
        delete_action = menu.addAction("Удалить")
        action = menu.exec_(self.window.task_viewer_demo.viewport().mapToGlobal(position))

        if action == edit_action:
            self.open_edit_task_window(task_id)
            

        elif action == delete_action:
            self.delete_task(task_id)  


    def delete_task(self, task_id):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить эту задачу?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success = self.orm.delete_task(task_id)
            if success:
                QMessageBox.information(self, "Успех", "Задача удалена")
                self.load_data()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось удалить задачу")

  


    def open_edit_task_window(self, task_id):
        if self.edit_task_window is None:
            self.edit_task_window = EditTaskWindow(task_id)
            self.edit_task_window.exec()  
            self.edit_task_window = None
        else:
            self.edit_task_window.load_task_data()
            self.edit_task_window.exec()
                        
        
    def open_calendar(self):
        if self.calendar_window == None:
            self.calendar_window = CalendarWindow(self.user_id, self.current_task_id)
        self.calendar_window.show() 


    def open_view_tasks_window(self):
        if self.view_tasks_window == None:
            self.view_tasks_window = ViewDictWindow(self.user_id)
        else:
            self.view_tasks_window.load_data_detalied()   
        self.view_tasks_window.show()    
        



        