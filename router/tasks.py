from fastapi import APIRouter, Form, Request,HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from model.handle_db import HandleDB
from model.user_db import UserDB
from model.categories_db import CategoriesDB
from model.status_db import StatusDB
from model.tasks_db import TaskDB

router = APIRouter()
template = Jinja2Templates(directory="./view")

#Consultas DB
db = HandleDB()
udb = UserDB()
cdb = CategoriesDB()
sdb = StatusDB()
tdb = TaskDB()

@router.get('/tasks', response_class=HTMLResponse)
def get_dashboard(req: Request):
    # Verificar si el usuario ha iniciado sesión
    username = req.cookies.get('username')
    if not username:
        return RedirectResponse(url='/', status_code=303)
    
    # Consultas
    categories = cdb.get_all_categories()
    users = udb.get_all_users()
    status = sdb.get_all_status()
    tasks = tdb.get_all_tasks()
    Open_tasks = tdb.get_open_tasks()
    progress_tasks = tdb.get_progress_tasks()
    completed_tasks = tdb.get_completed_tasks()
    count_status = tdb.status_count()
    
    return template.TemplateResponse(
        'tasks.html',
        {
            'request': req, 
            "username": username,
            'categories': categories,
            'users': users,
            'status': status,
            'Open_tasks': Open_tasks,
            'tasks': tasks,
            'progress_tasks':progress_tasks,
            'completed_tasks': completed_tasks,
            'count_status': count_status
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
        tdb.create_task(
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
    task = tdb.get_task_by_id(task_id)
    categories = cdb.get_all_categories()
    users = udb.get_all_users()
    status = sdb.get_all_status()
    tasks = tdb.get_all_tasks()
    Open_tasks = tdb.get_open_tasks()
    progress_tasks = tdb.get_progress_tasks()
    completed_tasks = tdb.get_completed_tasks()
    count_status = tdb.status_count()
    
    return template.TemplateResponse('edit_task.html',
         {
            'request': req,
            'task': task,
            'username': username,
            'categories': categories,
            'users': users,
            'status': status,
            'tasks': tasks,
            'progress_tasks':progress_tasks,
            'completed_tasks': completed_tasks,
            'Open_tasks': Open_tasks,
            'count_status': count_status
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
        tdb.update_task(
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