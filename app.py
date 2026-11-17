from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Literal
from datetime import datetime

app = FastAPI(title="ChatPayGuard API", version="0.1.0")


@app.get("/health")
async def health_check() -> dict:
    """Simple health endpoint."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


class TransactionPreviewRequest(BaseModel):
    merchant_name: str = Field(..., example="Acme Store")
    amount_cents: int = Field(..., gt=0, description="Amount in smallest currency unit")
    currency: Literal["USD", "EUR", "GBP"] = Field(..., example="USD")
    card_last4: str = Field(..., regex=r"^\d{4}$", description="Last 4 digits of the card")
    description: str | None = Field(None, example="Purchase of widgets")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @validator("amount_cents")
    def format_amount(cls, v):
        if v > 10_000_000:
            raise ValueError("Amount exceeds allowed limit")
        return v


class TransactionPreviewResponse(BaseModel):
    preview_id: str
    summary: str
    requires_confirmation: bool
    expires_at: datetime


def _generate_preview_id() -> str:
    """Simple deterministic preview identifier."""
    return f"preview-{int(datetime.utcnow().timestamp())}"


def _build_summary(req: TransactionPreviewRequest) -> str:
    amount = f"{req.amount_cents/100:.2f} {req.currency}"
    return (
        f"Purchase at {req.merchant_name}: {amount} "
        f"using card **** **** **** {req.card_last4}."
    )


@app.post("/preview", response_model=TransactionPreviewResponse)
async def preview_transaction(req: TransactionPreviewRequest) -> TransactionPreviewResponse:
    """
    Generate a preview of a transaction before exposing full card details.
    The client can use the returned `preview_id` to confirm or reject the payment.
    """
    if req.amount_cents > 5_000_00:  # example threshold for manual review
        requires_confirmation = True
    else:
        requires_confirmation = False

    preview_id = _generate_preview_id()
    summary = _build_summary(req)
    expires_at = datetime.utcnow().replace(microsecond=0) + timedelta(minutes=5)

    return TransactionPreviewResponse(
        preview_id=preview_id,
        summary=summary,
        requires_confirmation=requires_confirmation,
        expires_at=expires_at,
    )
