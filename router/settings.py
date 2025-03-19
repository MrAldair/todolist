from fastapi import APIRouter, Form, Request,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB
from model.categories_db import CategoriesDB
from model.status_db import StatusDB
from model.positions_db import PositionsDB

router = APIRouter()
template = Jinja2Templates(directory="./view")

db = HandleDB()
cdb = CategoriesDB()
sdb = StatusDB()
pdb = PositionsDB()

@router.get('/settings', response_class=HTMLResponse)
def get_settings(req: Request):
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)
    
    positions = pdb.get_all_positions()
    categories = cdb.get_all_categories()
    status = sdb.get_all_status()
    
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
        pdb.create_position(position=position)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la posición: {e}")

@router.post('/settings/status', response_class=RedirectResponse)
def add_status(status: str = Form(...)):
    try:
        sdb.create_status(status=status)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el status: {e}")

@router.post('/settings/category', response_class=RedirectResponse)
def add_category(category: str = Form(...)):
    try:
        cdb.create_category(category=category)
        return RedirectResponse(url='/settings', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la categoría: {e}")
