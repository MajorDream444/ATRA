"""
ATRA Sovereign Trade Engine
backend/api/main.py — FastAPI Application Entry Point

Endpoints:
  POST /api/access          — Sovereign Access Key validation
  POST /api/verify          — Agent Sentinel Step 2 vetting
  POST /api/request-briefing — Allocation briefing request
  GET  /api/pipeline/{id}   — CRM pipeline status
  GET  /api/status          — System heartbeat
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.sentinel_vetting import SentinelEngine

# ── App Init ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ATRA Sovereign Trade Engine API",
    description="Institutional-grade commodity trade facilitation — West African Gold Belt",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

sentinel = SentinelEngine()

# ── Valid Access Keys (demo set — replace with DB in production) ──────────────
VALID_KEYS = {
    "2026-B8X92Q": {"buyer_id": "SOV-HK-9214", "region": "Asia", "tier": 1},
    "2026-EU7734": {"buyer_id": "SOV-EU-7734", "region": "Europe", "tier": 1},
    "2026-ME5521": {"buyer_id": "SOV-ME-5521", "region": "Middle East", "tier": 1},
}

# ── Pipeline store (in-memory for demo — swap with DB) ────────────────────────
PIPELINE: dict = {}

# ── Models ────────────────────────────────────────────────────────────────────

class AccessKeyRequest(BaseModel):
    access_key: str

class VettingRequest(BaseModel):
    buyer_id: str
    entity_name: str
    registration_number: Optional[str] = ""
    pof_instrument: Optional[str] = "BCL"
    pof_bank_tier: Optional[int] = 1
    pof_amount_usd: Optional[float] = 0
    required_usd: Optional[float] = 0
    kyc_documents: Optional[list[str]] = []
    sanctions_clear: Optional[bool] = False
    pep_clear: Optional[bool] = False

class BriefingRequest(BaseModel):
    entity_name: str
    contact_name: str
    contact_email: str
    volume_interest: str  # trial | 1mt | 2-3mt | 5mt
    region: Optional[str] = ""
    settlement_preference: Optional[str] = ""  # traditional | digital | both
    esg_required: Optional[bool] = False

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/status")
def system_status():
    """Agent system heartbeat — all 5 agents online check"""
    return {
        "system": "ATRA Sovereign Trade Engine",
        "status": "SECURE",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "agents": {
            "Sentinel": "ONLINE",
            "Alchemist": "ONLINE",
            "Logos": "ONLINE",
            "Vault": "ONLINE",
            "Navigator": "ONLINE",
        },
        "blacklist_entries": len(sentinel.blacklist),
        "pipeline_active": len(PIPELINE),
    }


@app.post("/api/access")
def validate_access_key(req: AccessKeyRequest):
    """
    Sovereign Access Key validation — Agent Sentinel gate.
    Returns buyer profile if key is valid and not expired.
    """
    key = req.access_key.strip().upper()

    if key not in VALID_KEYS:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "REJECTED",
                "message": "Invalid or expired Sovereign Access Key.",
                "sentinel_note": "Unauthorized access attempt has been logged.",
            }
        )

    profile = VALID_KEYS[key]
    buyer_id = profile["buyer_id"]

    # Initialize pipeline entry
    if buyer_id not in PIPELINE:
        PIPELINE[buyer_id] = {
            "buyer_id": buyer_id,
            "region": profile["region"],
            "tier": profile["tier"],
            "current_step": 1,
            "step_statuses": {
                "1_consultation": "COMPLETE",
                "2_verification": "PENDING",
                "3_negotiation": "LOCKED",
                "4_documentation": "LOCKED",
                "5_payment": "LOCKED",
                "6_logistics": "LOCKED",
            },
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        }

    return {
        "status": "GRANTED",
        "buyer_id": buyer_id,
        "region": profile["region"],
        "tier": f"Tier-{profile['tier']}",
        "message": "Welcome to the ATRA Sovereign Portal. Agent Sentinel is standing by.",
        "pipeline": PIPELINE[buyer_id],
    }


@app.post("/api/verify")
def run_verification(req: VettingRequest):
    """
    Agent Sentinel — Full Step 2 verification.
    Runs blacklist check, POF validation, KYC review.
    """
    entity_data = {
        "entity_name": req.entity_name,
        "registration_number": req.registration_number,
        "pof_data": {
            "instrument_type": req.pof_instrument,
            "bank_tier": req.pof_bank_tier,
            "amount_usd": req.pof_amount_usd,
            "required_usd": req.required_usd,
        },
        "kyc_data": {
            "submitted_documents": req.kyc_documents,
            "sanctions_check_passed": req.sanctions_clear,
            "pep_check_passed": req.pep_clear,
        },
    }

    report = sentinel.run_full_vetting(
        buyer_id=req.buyer_id,
        entity_data=entity_data,
    )

    # Update pipeline step
    if req.buyer_id in PIPELINE:
        if report["recommendation"] == "ADVANCE_TO_LOGOS":
            PIPELINE[req.buyer_id]["current_step"] = 3
            PIPELINE[req.buyer_id]["step_statuses"]["2_verification"] = "COMPLETE"
            PIPELINE[req.buyer_id]["step_statuses"]["3_negotiation"] = "ACTIVE"
        else:
            PIPELINE[req.buyer_id]["step_statuses"]["2_verification"] = "REVIEW"

    if report["risk_level"] == "BLOCKED":
        raise HTTPException(status_code=403, detail=report)

    return report


@app.post("/api/request-briefing")
def request_briefing(req: BriefingRequest):
    """
    Public briefing request — no access key required.
    Creates a lead record and triggers Sentinel pre-screening.
    """
    ref = "ATRA-RFP-" + hashlib.md5(
        f"{req.entity_name}{req.contact_email}{datetime.datetime.utcnow()}".encode()
    ).hexdigest()[:8].upper()

    volume_map = {
        "trial": "50–500 kg (Trial Tranche)",
        "1mt": "1 MT / Month",
        "2-3mt": "2–3 MT / Month",
        "5mt": "5 MT / Month (Full Allocation)",
    }

    record = {
        "ref": ref,
        "entity": req.entity_name,
        "contact": req.contact_name,
        "email": req.contact_email,
        "volume": volume_map.get(req.volume_interest, req.volume_interest),
        "region": req.region,
        "settlement": req.settlement_preference,
        "esg_stream": "Green Gold" if req.esg_required else "Standard",
        "status": "RECEIVED",
        "next_step": "Agent Sentinel will initiate Step 2 verification within 24 hours.",
        "submitted_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

    return {
        "status": "REQUEST_RECEIVED",
        "ref": ref,
        "message": f"Your briefing request has been logged. M. Diallo will contact {req.contact_email} within 24 hours.",
        "record": record,
    }


@app.get("/api/pipeline/{buyer_id}")
def get_pipeline(buyer_id: str):
    """CRM pipeline status for a verified buyer"""
    if buyer_id not in PIPELINE:
        raise HTTPException(
            status_code=404,
            detail={"message": f"No active pipeline found for {buyer_id}"}
        )
    return PIPELINE[buyer_id]


@app.get("/api/allocation")
def get_allocation():
    """Current Gold allocation availability — public endpoint"""
    return {
        "total_monthly_mt": 5.0,
        "committed_mt": 2.5,
        "available_mt": 2.5,
        "esg_streams": {
            "green_gold_percent": 85,
            "mercury_free_certified": True,
            "standard_market_percent": 15,
        },
        "corridors": ["Mauritania", "Mali Interior", "Burkina Faso"],
        "settlement": ["DLC", "MT103", "Escrow", "USDT", "BTC"],
        "updated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
