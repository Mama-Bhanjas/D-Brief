from fastapi import FastAPI
from .database import engine, Base
from .routes import reports, summaries
from .config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Disaster Information Summarization Platform API"}
