import sqlite3
from model.handle_db import HandleDB

class PositionsDB(HandleDB):
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