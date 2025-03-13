from fastapi import APIRouter,FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from router.signup import router as signup_router

app = FastAPI()
template = Jinja2Templates(directory='./view')

@app.get('/', response_class=HTMLResponse)
def index(req: Request):
    return template.TemplateResponse('index.html', {'request': req})



app.include_router(signup_router)