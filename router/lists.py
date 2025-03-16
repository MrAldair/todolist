from fastapi import APIRouter, Form, Request,HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB

router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()


@router.get('/lists', response_class=HTMLResponse)
def get_dashboard(req: Request):
    # Verificar si el usuario ha iniciado sesión
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)

    # Consultas
    categories = db.get_all_categories()
    users = db.get_all_users()
    status = db.get_all_status()

    print(users)
    print(status)
    

    return template.TemplateResponse(
        'lists.html',
        {
            'request': req, 
            "username": username,
            'categories': categories,
            'users': users,
            'status': status
        }
    )