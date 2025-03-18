from fastapi import APIRouter, Form, Request,HTTPException, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB

router = APIRouter()
template = Jinja2Templates(directory="./view")
db = HandleDB()


@router.get('/tasks', response_class=HTMLResponse)
def get_dashboard(req: Request):
    # Verificar si el usuario ha iniciado sesión
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)

    # Consultas
    categories = db.get_all_categories()
    users = db.get_all_users()
    status = db.get_all_status()
    tasks = db.get_all_tasks()

    return template.TemplateResponse(
        'tasks.html',
        {
            'request': req, 
            "username": username,
            'categories': categories,
            'users': users,
            'status': status,
            'tasks': tasks
        }
    )

@router.post('/tasks', response_class=RedirectResponse)
def add_task(
    req: Request,
    task: str = Form(...),
    category_id: int = Form(...),
    details: str = Form(...),
    created: str = Form(...),
    user_id: int = Form(...),
    status_id: int = 1
):
    try:
        db.create_task(
            task=task,
            category_id=category_id,
            details=details,
            created=created,
            user_id=user_id,
            status_id=status_id
        )
        return RedirectResponse(url='/tasks', status_code=303)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al guardar la tarea: {e}",
        )
    
@router.get('/editTask/{task_id}', response_class=HTMLResponse)
def edit_task(req: Request, task_id: int):
    # Verificar si el usuario ha iniciado sesión
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)
    task = db.get_task_by_id(task_id)
    categories = db.get_all_categories()
    users = db.get_all_users()
    status = db.get_all_status()
    tasks = db.get_all_tasks()

    return template.TemplateResponse('edit_task.html',
         {
            'request': req,
            'task': task,
            'username': username,
            'categories': categories,
            'users': users,
            'status': status,
            'tasks': tasks
        }
    )
@router.post('/updateTask/{task_id}', response_class=HTMLResponse)
def update_task(
    req: Request,
    task_id: int,
    task: str = Form(...),
    category_id: int = Form(...),
    details: str = Form(...),
    user_id: int = Form(...),
    status_id: int = Form(...)
):
    try:
        db.update_task(
            task_id=task_id,
            task=task,
            category_id=category_id,
            details=details,
            user_id=user_id,
            status_id=status_id
        )

        return RedirectResponse(url='/tasks', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el task: {e}")