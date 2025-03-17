import sqlite3

#----------------Database Conexion----------------
class HandleDB():
    def __init__(self, db_path="./task_data.db"):
        self.db_path = db_path
        
#----Crear una nueva conexion para cada solicitud
    def _connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
#------------Users table-------------------------

    def insert(self, data_user):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, position_id, username, password) VALUES (?, ?, ?, ?, ?)",
                    (data_user['firstname'], data_user['lastname'], data_user['position_id'], data_user['username'], data_user['password']))
        conn.commit()
        conn.close()
        
    def get_only(self, data_user):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (data_user,))
        data = cur.fetchone()
        conn.close()
        return data
    
    #obtiene el user_id del usuario
    def get_user_id_by_username(self, username: str):
        user_data = self.get_only(username)
        if user_data:
            return user_data[4]  
        return None
    

    def get_all_users(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT user_id, firstname || ' ' || lastname as name FROM users")
                users = [{"user_id": row[0], "name": row[1]} for row in cur.fetchall()]
                return users
        except sqlite3.Error as e:
            print(f"Error al obtener todos los usuarios {e}")
            raise

#---------------------Categories--------------------------------
    def get_all_categories(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT category_id, category FROM categories")
                categories = [{"category_id": row[0], "category": row[1]} for row in cur.fetchall()]
                return categories
        except sqlite3.Error as e:
            print(f"Error al obtener todas las categorias {e}")
            raise

#---------------------Status--------------------------------

    def get_all_status(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT status_id, status FROM status")
                status = [{"status_id": row[0], "status": row[1]} for row in cur.fetchall()]
                return status
        except sqlite3.Error as e:
            print(f"Error al obtener todas las status: {e}")
            raise

#---------------------Positions--------------------------------

    def get_all_positions(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("SELECT position_id, position FROM positions")
                positions = [{"position_id": row[0], "position": row[1]} for row in cur.fetchall()]
                return positions
        except sqlite3.Error as e:
            print(f"Error al obtener todas las posiciones: {e}")
            raise

#---------------------Tasks--------------------------------
    def get_all_tasks(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                            SELECT
                                t.task_id,
                                t.task,
                                t.details,
                                STRFTIME('%m-%d-%Y', t.created) AS Created,
                                s.status AS status,
                                c.category AS Category,
                                u.firstname || ' ' || u.lastname AS user_name,
                                t.updated
                            FROM tasks t
                            LEFT JOIN status s ON t.status_id = s.status_id
                            LEFT JOIN categories c ON t.category_id = c.category_id
                            LEFT JOIN users u ON t.user_id = u.user_id;""")
                tasks = [{"task_id": row[0], "task": row[1], "details": row[2], "Created on": row[3],
                           "status_id": row[4], "category_id": row[5], "user_name": row[6], "updated": row[7]} for row in cur.fetchall()]
                return tasks
        except sqlite3.Error as e:
            print(f"Error al obtener todas las tasks: {e}")
            raise
