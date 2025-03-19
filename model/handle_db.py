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