import sqlite3 as sq
from datetime import datetime, timedelta


class ORM:
    def __init__(self, dbname):
        self.dbname = dbname + '.db'
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)""")
            
            
            cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
                        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        task_name TEXT NOT NULL,
                        description TEXT,
                        date TEXT,
                        start_time TEXT,
                        duration TEXT,
                        remind_before TEXT,
                        status TEXT DEFAULT'Не начата', 
                        FOREIGN KEY (user_id) REFERENCES users(user_id))""") 
                
                



    def reg_user(self, username, password):
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO users (username, password) VALUES(?,?)""",(username, password))

            
    def log_user(self, username, password):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("""SELECT user_id FROM
                            users WHERE username = ? AND password = ? """, (username, password))
                user = cur.fetchone()
                return user[0] if user else None
        except Exception as e:
            print(f'Ошибка при входе: {str(e)}')
            return None   
        




    def insert_task(self, user_id, task_name):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO tasks 
                        (user_id,
                        task_name) VALUES(?, ?)""", 
                        (user_id, task_name))
                task_id = cur.lastrowid
                con.commit()
                return task_id
        except Exception as e:
            print(f'Ошибка при добавлении слова: {str(e)}')
            return False
                 

    def update_task(self, task_id, task_name, date = None, start_time=None, duration=None, remind_before=None, description=None):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("""UPDATE tasks
                            SET task_name = ?,
                            description = COALESCE(?, description),
                            date = COALESCE(?, date),
                            start_time = COALESCE(?, start_time),
                            duration = COALESCE(?, duration),
                            remind_before = COALESCE(?, remind_before)
                            WHERE task_id = ?""",
                            (task_name, description, date, start_time, duration, remind_before,  task_id))
                con.commit()
                return True
        except Exception as e:
            print(f'Ошибка при обновлении задачи: {str(e)}')  
            return False





    def set_status(self):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
            
                cur.execute("""
                    SELECT task_id, date, start_time, duration FROM tasks 
                    WHERE date IS NOT NULL AND start_time IS NOT NULL AND duration IS NOT NULL
                """)
                rows = cur.fetchall()

                current_dt = datetime.now()
                for row in rows:
                    task_id, date_str, start_time_str, duration_str = row
                    try:
                        task_date = datetime.strptime(date_str, "%Y-%m-%d")
                        start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
                        duration_time = datetime.strptime(duration_str, "%H:%M:%S").time()
                        start_dt = datetime.combine(task_date, start_time)
                        duration_delta = timedelta(
                            hours=duration_time.hour,
                            minutes=duration_time.minute,
                            seconds=duration_time.second
                        )
                        end_dt = start_dt + duration_delta
            
                        if current_dt < start_dt:
                            status = "Запланирована"
                        elif start_dt <= current_dt <= end_dt:
                            status = "В процессе"
                        elif current_dt > end_dt:
                            status = "Просрочена"
                        else:
                            status = "Запланирована"
                    except Exception as e:
                        print(f"Ошибка парсинга времени задачи {task_id}: {e}")
                        status = "Ошибка"

                    cur.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
                con.commit()
        except Exception as e:
            print(f"Ошибка при обновлении статусов: {e}")    
        

    def get_data(self, user_id):
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""SELECT task_name FROM tasks WHERE user_id = ?""", (user_id,))    
            rows = cur.fetchall()
            return rows
        



    def get_data_detalied(self, user_id):
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""
                SELECT task_name, description, date, start_time, duration, remind_before,status 
                FROM tasks WHERE user_id = ?
            """, (user_id,))
            rows = cur.fetchall()
            return rows
    


    def get_date(self, task_id):
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""SELECT date FROM tasks WHERE task_id =?""", (task_id,))
        date = cur.fetchone()
        return date[0] if date else None 
    def get_task_by_id(self, task_id):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
                return cur.fetchone()
        except Exception as e:
            print(f"Error getting task: {e}")
            return None


    def get_task_id_by_name(self, user_id, task_name):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
                cur.execute("SELECT task_id FROM tasks WHERE user_id = ? AND task_name = ?", 
                        (user_id, task_name))
                result = cur.fetchone()
                return result[0] if result else None
        except Exception as e:
            print(f"Error getting task_id: {e}")
            return None

    
    
    def replace_task_data(self, task_id, date, start_time, duration, remind_before, description):
        with sq.connect(self.dbname) as con:
            cur = con.cursor()
            cur.execute("""UPDATE tasks
                        SET date = ?, start_time = ?, duration = ?, remind_before = ?, description = ?
                        WHERE task_id = ? """,(date, start_time, duration,  remind_before, description, task_id))
        return True


    def delete_task(self, task_id):
        try:
            with sq.connect(self.dbname) as con:
                cur = con.cursor()
            
                cur.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
                con.commit()
            return True
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False    