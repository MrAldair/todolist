from fastapi import APIRouter, Form, Request,HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB

router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()

@router.get('/settings', response_class=HTMLResponse)
def get_settings(req: Request):
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)
    
    positions = db.get_all_positions()
    categories = db.get_all_categories()
    status = db.get_all_status()
    
    return template.TemplateResponse(
        'settings.html',
        {
            'request': req,
            'username': username,
            'positions': positions,
            'categories': categories,
            'status': status
        }
    )
    
@router.post('/settings/position', response_class=RedirectResponse)
def add_position(position: str = Form(...)):
    try:
        db.create_position(position=position)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la posición: {e}")

@router.post('/settings/status', response_class=RedirectResponse)
def add_status(status: str = Form(...)):
    try:
        db.create_status(status=status)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el status: {e}")

@router.post('/settings/category', response_class=RedirectResponse)
def add_category(category: str = Form(...)):
    try:
        db.create_category(category=category)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la categoría: {e}")
