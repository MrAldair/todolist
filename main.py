from fastapi import FastAPI
from router.signup import router as signup_router
from router.index import router as index_router
from router.dashboard import router as dashboard_router
from router.tasks import router as tasks_router
from router.settings import router as settings_router

app = FastAPI()

app.include_router(signup_router)
app.include_router(index_router)
app.include_router(dashboard_router)
app.include_router(tasks_router)
app.include_router(settings_router)