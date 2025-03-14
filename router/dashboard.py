from fastapi import APIRouter, FastAPI, Form, Request,HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user
from model.handle_db import HandleDB


router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()

@router.get('/dashboard', response_class=HTMLResponse)
def get_dashboard(req: Request):
    return RedirectResponse('/')
    #return template.TemplateResponse('dashboard.html', {'request': req})

@router.post('/dashboard', response_class=HTMLResponse)
def post_dashboard(req: Request, username: str = Form(), password: str = Form()):
    verify = check_user(username, password)
    if verify: 
        return template.TemplateResponse('dashboard.html', {'request': req, 'data_user': verify})
    return RedirectResponse('/')