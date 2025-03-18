import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo

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
    def create_category(self, category):
        """Crea una nueva category."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO categories (category) 
                    VALUES (?)
                """, ( category,))
                conn.commit()
                return cur.lastrowid  # Devuelve el ID de la tarea creada
        except sqlite3.Error as e:
            print(f"Error al crear la posicion '{category}': {e}")
            raise
    
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

    def create_status(self, status):
        """Crea una nueva posicion."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO status (status) 
                    VALUES (?)
                """, ( status,))
                conn.commit()
                return cur.lastrowid  # Devuelve el ID de la tarea creada
        except sqlite3.Error as e:
            print(f"Error al crear el status '{status}': {e}")
            raise
    
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

    def create_position(self, position):
        """Crea una nueva posicion."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO positions (position) 
                    VALUES (?)
                """, ( position,))
                conn.commit()
                return cur.lastrowid  # Devuelve el ID de la tarea creada
        except sqlite3.Error as e:
            print(f"Error al crear la posicion '{position}': {e}")
            raise
    
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

    def create_task(self, task, details, created, status_id, category_id, user_id):
        """Crea una nueva tarea."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO tasks (task, details, created, status_id, category_id, user_id) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (task, details, created, status_id, category_id, user_id))
                conn.commit()
                return cur.lastrowid  # Devuelve el ID de la tarea creada
        except sqlite3.Error as e:
            print(f"Error al crear la tarea '{task}': {e}")
            raise

    def get_task_by_id(self, task_id):
        """Obtiene una tarea por su ID."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT task_id, task, details, created, status_id, category_id, user_id, updated 
                    FROM tasks WHERE task_id = ?
                """, (task_id,))
                row = cur.fetchone()
                return {
                    "task_id": row[0],
                    "task": row[1],
                    "details": row[2],
                    "created": row[3],
                    "status_id": row[4],
                    "category_id": row[5],
                    "user_id": row[6],
                    "updated": row[7]
                } if row else None
        except sqlite3.Error as e:
            print(f"Error al obtener la tarea con ID {task_id}: {e}")
            raise

    def update_task(self, task_id, task=None, details=None, status_id=None, category_id=None, user_id=None):
        """Actualiza una tarea por su ID."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()

                # Generar la consulta dinámicamente según los valores proporcionados
                updates = []
                params = []
                
                if task:
                    updates.append("task = ?")
                    params.append(task)
                if details:
                    updates.append("details = ?")
                    params.append(details)
                if status_id:
                    updates.append("status_id = ?")
                    params.append(status_id)
                if category_id:
                    updates.append("category_id = ?")
                    params.append(category_id)
                if user_id:
                    updates.append("user_id = ?")
                    params.append(user_id)
                if not updates:
                    return 0  # No hay cambios
                
                # Agregar la fecha de actualización
                updated_time = datetime.now(ZoneInfo("America/Tijuana")).strftime('%H:%M:%S %m-%d-%Y')
                updates.append("updated = ?")
                params.append(updated_time)  
                
                params.append(task_id)

                query = f"UPDATE tasks SET {', '.join(updates)} WHERE task_id = ?"
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount  # Devuelve el número de filas afectadas
        except sqlite3.Error as e:
            print(f"Error al actualizar la tarea con ID {task_id}: {e}")
            raise

    def delete_task(self, task_id):
        """Elimina una tarea por su ID."""
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
                conn.commit()
                return cur.rowcount  # Devuelve el número de filas eliminadas
        except sqlite3.Error as e:
            print(f"Error al eliminar la tarea con ID {task_id}: {e}")
            raise
        
#--------------------------Consulta task por status----------------------------
    def get_open_tasks(self):
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
                            LEFT JOIN users u ON t.user_id = u.user_id
                            WHERE t.status_id = 1;""")
                tasks = [{"task_id": row[0], "task": row[1], "details": row[2], "Created on": row[3],
                           "status_id": row[4], "category_id": row[5], "user_name": row[6], "updated": row[7]} for row in cur.fetchall()]
                return tasks
        except sqlite3.Error as e:
            print(f"Error al obtener todas las tasks: {e}")
            raise
        
    def get_progress_tasks(self):
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
                            LEFT JOIN users u ON t.user_id = u.user_id
                            WHERE t.status_id = 2;""")
                tasks = [{"task_id": row[0], "task": row[1], "details": row[2], "Created on": row[3],
                           "status_id": row[4], "category_id": row[5], "user_name": row[6], "updated": row[7]} for row in cur.fetchall()]
                return tasks
        except sqlite3.Error as e:
            print(f"Error al obtener todas las tasks: {e}")
            raise
        
    def get_completed_tasks(self):
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
                            LEFT JOIN users u ON t.user_id = u.user_id
                            WHERE t.status_id = 3;""")
                tasks = [{"task_id": row[0], "task": row[1], "details": row[2], "Created on": row[3],
                           "status_id": row[4], "category_id": row[5], "user_name": row[6], "updated": row[7]} for row in cur.fetchall()]
                return tasks
        except sqlite3.Error as e:
            print(f"Error al obtener todas las tasks: {e}")
            raise
        
    def status_count(self):
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute("""
                    SELECT
                        COUNT(*) as Total,
                        SUM(CASE WHEN s.status_id = 1 THEN 1 ELSE 0 END) AS Open,
                        SUM(CASE WHEN s.status_id = 2 THEN 1 ELSE 0 END) AS InProgress,
                        SUM(CASE WHEN s.status_id = 3 THEN 1 ELSE 0 END) AS Completed
                    FROM tasks t
                    LEFT JOIN status s ON t.status_id = s.status_id;
                """)
                row = cur.fetchone()

                total = row[0] or 1  # Previene la división por cero si no hay tareas.
                open_count = row[1]
                in_progress_count = row[2]
                completed_count = row[3]

                # Calculamos los porcentajes
                open_percentage = (open_count / total) * 100
                in_progress_percentage = (in_progress_count / total) * 100
                completed_percentage = (completed_count / total) * 100

                count_status = {
                    'Total': total,
                    'Open': open_count,
                    'InProgress': in_progress_count,
                    'Completed': completed_count,
                    'OpenPercentage': round(open_percentage, 2),
                    'InProgressPercentage': round(in_progress_percentage, 2),
                    'CompletedPercentage': round(completed_percentage, 2)
                }

                return count_status
        except sqlite3.Error as e:
            print(f"Error al obtener todas las tasks: {e}")
            raise

