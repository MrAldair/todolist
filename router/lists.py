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

    return template.TemplateResponse(
        'lists.html',
        {
            'request': req, 
            "username": username,
        }
    )