import sqlite3
from model.handle_db import HandleDB

class CategoriesDB(HandleDB):
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