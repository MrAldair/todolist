from fastapi import APIRouter, FastAPI, Form, Request,HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user
from model.handle_db import HandleDB


router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()

#Dependencia para verificar autenticacion
def get_current_user(req: Request):
    username = req.cookies.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No has iniciado sesion"
        )
    return username
'''
@router.get('/dashboard', response_class=HTMLResponse)
def get_dashboard(req: Request):
    return RedirectResponse('/')
    #return template.TemplateResponse('dashboard.html', {'request': req})

@router.post('/dashboard', response_class=HTMLResponse)
def post_dashboard(req: Request, username: str = Form(), password: str = Form()):
    verify = check_user(username, password)
    if verify:
        return template.TemplateResponse('dashboard.html', {'request': req, 'data_user': verify})
    return RedirectResponse('/')'
    '''
#Dependencia para verificar autenticacion
def get_current_user(req: Request):
    username = req.cookies.get("username")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No has iniciado sesion"
        )
    return username

@router.post('/dashboard', response_class=HTMLResponse)
def post_dashboard(req: Request, username: str = Form(), password: str = Form()):
    verify = check_user(username, password)
    if verify:
        print(f"Inicio de sesion exitoso de usuario: {username}")
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="username", value=username)
        return response
    else:
        print(f"Error en la autenticacion para el usuario: {username}")
        return RedirectResponse(url="/", status_code=303)
    
@router.get('/dashboard', response_class=HTMLResponse)
def get_dashboard(req: Request):
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)
    return template.TemplateResponse(
        'dashboard.html',
        {
            'request':req,
            'username': username
        }
        )