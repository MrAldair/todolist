from fastapi import APIRouter,FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from router.signup import router as signup_router
from router.dashboard import router as dashboard_router
from router.index import router as index_router

app = FastAPI()
template = Jinja2Templates(directory='./view')


app.include_router(signup_router)
app.include_router(index_router)
app.include_router(dashboard_router)