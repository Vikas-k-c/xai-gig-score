from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.pan import PanDetails
from ..models.user import User
from ..schemas.pan import PanResponse, PanSubmitRequest
from ..utils.validators import validate_pan
from .auth import get_current_user


router = APIRouter(prefix="/pan", tags=["pan"])


@router.post("/submit", response_model=PanResponse, status_code=status.HTTP_201_CREATED)
def submit_pan(
    payload: PanSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PanResponse:
    pan_number = payload.pan_number.strip().upper()

    if not validate_pan(pan_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PAN format",
        )

    existing_pan_for_other_user = (
        db.query(PanDetails)
        .filter(PanDetails.pan_number == pan_number, PanDetails.user_id != current_user.id)
        .first()
    )
    if existing_pan_for_other_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PAN already linked to another user",
        )

    existing_pan = db.query(PanDetails).filter(PanDetails.user_id == current_user.id).first()

    if existing_pan:
        existing_pan.pan_number = pan_number
        existing_pan.is_verified = True
        db.commit()
        db.refresh(existing_pan)
        return existing_pan

    pan_record = PanDetails(
        user_id=current_user.id,
        pan_number=pan_number,
        is_verified=True,  # mock verification
    )
    db.add(pan_record)
    db.commit()
    db.refresh(pan_record)

    return pan_record


@router.get("/", response_model=PanResponse)
def get_pan_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PanResponse:
    pan_record = db.query(PanDetails).filter(PanDetails.user_id == current_user.id).first()

    if not pan_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PAN not submitted yet",
        )

    return pan_record