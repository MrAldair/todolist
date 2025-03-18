import sqlite3
from model.handle_db import HandleDB

class UserDB(HandleDB):
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