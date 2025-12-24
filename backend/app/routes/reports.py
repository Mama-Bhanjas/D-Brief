from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.report import Report
from ..schemas.report import ReportCreate, ReportResponse
from ..services.verification import VerificationService
from ..services.ai_pipeline import ai_pipeline

router = APIRouter()

@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    # 1. Verify Source
    verification_result = VerificationService.verify_source(report.source_identifier, report.source_type)
    
    # 2. AI Processing (Simulated as synchronous for simplicity, would be async in prod)
    category = ai_pipeline.classify_report(report.text)
    
    db_report = Report(
        text=report.text,
        source_type=report.source_type,
        source_identifier=report.source_identifier,
        is_verified=verification_result["is_verified"],
        verification_status=verification_result["status"],
        disaster_category=category
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/{report_id}", response_model=ReportResponse)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

@router.get("/", response_model=List[ReportResponse])
def read_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = db.query(Report).offset(skip).limit(limit).all()
    return reports
