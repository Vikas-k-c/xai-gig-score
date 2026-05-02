from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .models import User, PanDetails, PlatformData, Prediction, Loan
from .routes.auth import router as auth_router
from .routes.pan import router as pan_router
from .routes.platform import router as platform_router
from .routes.predict import router as predict_router
from .routes.loans import router as loans_router
from .routes.dashboard import router as dashboard_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gig Credit Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(pan_router)
app.include_router(platform_router)
app.include_router(predict_router)
app.include_router(loans_router)
app.include_router(dashboard_router)