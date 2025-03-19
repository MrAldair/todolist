import sqlite3
from model.handle_db import HandleDB

class StatusDB(HandleDB):
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