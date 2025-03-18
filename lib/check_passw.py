from model.user_db import UserDB
from werkzeug.security import check_password_hash

def check_user(username, passw):
    user = UserDB()
    filter_user = user.get_only(username)
    if filter_user:
        same_passw = check_password_hash(filter_user[5], passw)
        if same_passw:
            return filter_user
        return None