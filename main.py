from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from database import Base, engine
from routers import users, assignments, submissions


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Assignment Submission App",
    description="API for managing users, assignments, and submissions using JWT auth.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app.include_router(users.router)
app.include_router(assignments.router)
app.include_router(submissions.router)
