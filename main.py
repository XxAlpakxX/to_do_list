from PySide6.QtWidgets import *
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
import sys
import sqlite3 as sq
from main_window import MainWindow

from orm import ORM

dict_orm = ORM('taskmanager')




class LoginWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.load_ui()
        self.setup_connections()
        self.setMinimumSize(400, 550)
        self.main_window = None
        self.current_user_id = None
        self.style_register_btn()
        self.style_login_btn()
        

    def load_ui(self):
        ui_file = QFile("RegistrationWindow.ui")
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        layout = QVBoxLayout(self)
        layout.addWidget(self.window)
        self.setLayout(layout)
        self.setWindowTitle('задачник')
       
        self.setMinimumSize(400, 450)
        



    def setup_connections(self):
        self.window.r_register_btn.clicked.connect(self.register)
        self.window.l_login_btn.clicked.connect(self.login)

        
    def style_register_btn(self):
        self.window.r_register_btn.setStyleSheet("""
            QPushButton {
                color: white;                    /* Цвет текста */
                background-color: #5495D6;       /* Цвет фона */
                border: 2px solid #FAFCFF;       /* Граница */
                border-radius: 20px;             /* Закругление углов */
                font-weight: bold;               /* Жирный шрифт */
                font-size: 14px;                 /* Размер шрифта */
                padding: 8px 16px;               /* Внутренние отступы */
            }
            QPushButton:hover {
                background-color: #144D82;       /* Цвет фона при наведении */
            }
            QPushButton:pressed {
                background-color: #3d8b40;       /* Цвет фона при нажатии */
            }
            QPushButton:disabled {
                background-color: #cccccc;       /* Цвет фона когда отключена */
                color: #666666;
            }
        """)
    
    def style_login_btn(self):
        self.window.l_login_btn.setStyleSheet("""
            QPushButton {
                color: white;                    /* Цвет текста */
                background-color: #5495D6;       /* Цвет фона */
                border: 2px solid #FAFCFF;       /* Граница */
                border-radius: 20px;             /* Закругление углов */
                font-weight: bold;               /* Жирный шрифт */
                font-size: 14px;                 /* Размер шрифта */
                padding: 8px 16px;               /* Внутренние отступы */
            }
            QPushButton:hover {
                background-color: #144D82;       /* Цвет фона при наведении */
            }
            QPushButton:pressed {
                background-color: #3d8b40;       /* Цвет фона при нажатии */
            }
            QPushButton:disabled {
                background-color: #cccccc;       /* Цвет фона когда отключена */
                color: #666666;
            }
        """)
    def show_error(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet('color: red;')

    def show_success(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet('color: green;')      


    def register_user(self, username, password):
        dict_orm.reg_user(username, password)


    def login_user(self, username, password):
        return dict_orm.log_user(username, password)



    def register(self):
        username = self.window.r_login.text().strip()
        password = self.window.r_password.text().strip()
        r_password_r = self.window.r_password_repeat.text().strip()

        if not username or not password or not r_password_r:
            QMessageBox.warning(self, "Ошибка", "заполните все поля")
            return
        
        elif password != r_password_r:
             QMessageBox.warning(self, "Ошибка", "Введённые пароли не совпадают")
             return
        
        try:
            self.register_user(username, password)
            QMessageBox.information(self, "Успех", "Пользователь добавлен")
            self.window.r_login.clear()
            self.window.r_password.clear()
            self.window.r_password_repeat.clear()

        except sq.IntegrityError:
            QMessageBox.warning(self, "Ошибка", "Такой пользователь уже есть")

        except Exception as e:
            print(f"Ошибка при регистрации: {e}")
   

    def login(self):
        username = self.window.l_login.text().strip()
        password = self.window.l_password.text().strip()
        if not username or not password:
            print('Поле не должно быть пустым')
        current_user = self.login_user(username, password) 
        if current_user:
            self.open_main_window(current_user)


    def open_main_window(self, user_id):
        self.main_window = MainWindow(user_id, self)
        self.main_window.show()
        self.hide()


app = QApplication(sys.argv)

window = LoginWindow()
window.show()
app.exec()
