from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.database.mongodb import db
from app.routes.workout import router as workout_router
from app.routes.bmi import router as bmi_router

app = FastAPI(
    title="GymPro API",
    version="1.0.0"
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

@app.get("/")
def home():
    return {"message": "GymPro Backend Running"}


@app.get("/db-test")
def db_test():
    db.command("ping")
    return {"message": "MongoDB Connected Successfully"}