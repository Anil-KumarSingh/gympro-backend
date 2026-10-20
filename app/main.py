from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.database.mongodb import db
from app.routes.workout import router as workout_router
from app.routes.bmi import router as bmi_router
from app.routes.complaint import router as complaint_router
from app.routes.admin import router as admin_router
from app.routes.dashboard import router as dashboard_router
from app.routes.nutrition import router as nutrition_router
from app.routes.workout import router as workout_router
from app.routes.bmi import router as bmi_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="GymPro API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        https://gympro-frontend-r6bp.onrender.com
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    workout_router,
    prefix="/workout",
    tags=["Workout"]
)

app.include_router(
    bmi_router,
    prefix="/bmi",
    tags=["BMI"]
)

app.include_router(
    complaint_router,
    prefix="/complaint",
    tags=["Complaint"]
)

app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)
app.include_router(
    nutrition_router,
    prefix="/nutrition",
    tags=["Nutrition"]
)

app.include_router(
    workout_router,
    prefix="/workout",
    tags=["Workout"]
)

app.include_router(
    bmi_router,
    prefix="/bmi",
    tags=["BMI"]
)

@app.get("/")
def home():
    return {"message": "GymPro Backend Running"}


@app.get("/db-test")
def db_test():
    db.command("ping")
    return {"message": "MongoDB Connected Successfully"}
