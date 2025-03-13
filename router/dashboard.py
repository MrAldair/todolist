from fastapi import APIRouter, FastAPI, Request,HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from controller.user import User
from lib.check_passw import check_user
from model.handle_db import HandleDB


router = APIRouter()
template = Jinja2Templates(directory="./view")

@router.get('/dashboard', response_class=HTMLResponse)
def get_dashboard(req: Request):
    return template.TemplateResponse('dashboard.html', {'request': req})