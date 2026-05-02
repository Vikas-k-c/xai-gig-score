from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.loan import Loan
from ..models.user import User
from ..schemas.loan import LoanApplyRequest, LoanResponse
from .auth import get_current_user


router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("/apply", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def apply_for_loan(
    payload: LoanApplyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> LoanResponse:
    loan = Loan(
        user_id=current_user.id,
        bank_name=payload.bank_name.strip(),
        amount=payload.amount,
        status="Pending",
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


@router.get("/", response_model=list[LoanResponse])
def list_loans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loans = (
        db.query(Loan)
        .filter(Loan.user_id == current_user.id)
        .order_by(Loan.created_at.desc())
        .all()
    )
    return loans