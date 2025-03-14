from fastapi import APIRouter, FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user
from model.handle_db import HandleDB

router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()

@router.get('/', response_class=HTMLResponse)
def index(req: Request):
    return template.TemplateResponse('index.html', {'request': req})