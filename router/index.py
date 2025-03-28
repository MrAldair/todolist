from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB

router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()

@router.get('/', response_class=HTMLResponse)
def index(req: Request):
    return template.TemplateResponse('index.html', {'request': req})

@router.get('/logout')
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="username")  # Eliminar la cookie de sesión
    return response