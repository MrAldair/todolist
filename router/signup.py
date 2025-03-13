from fastapi import APIRouter, FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user
from model.handle_db import HandleDB


router = APIRouter()
template = Jinja2Templates(directory="./view")

@router.get('/signup', response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse('signup.html', {'request': req})

@router.post('/signup', response_class=HTMLResponse)
def create_user(firstname: str = Form(), lastname: str = Form(), position_id: int = Form(), username: str = Form(), password: str = Form()):
    data_user = {
        'firstname': firstname,
        'lastname': lastname,
        'position_id': position_id,
        'username': username,
        'password': password,
    }
    db = User(data_user)
    db.create_user()
    return RedirectResponse('/', status_code=303)