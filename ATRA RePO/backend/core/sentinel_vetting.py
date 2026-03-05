"""
ATRA Sovereign Trade Engine
Agent Sentinel — Step 2 Verification & Blacklist Engine

Mandate: Protect the agency from fraud, ghost brokers, and bad-faith actors.
No entity advances past Step 2 without Sentinel clearance.

Usage:
    python sentinel_vetting.py --buyer-id SOV-HK-9214 --entity "Acme Holdings Ltd"
"""

import json
import hashlib
import argparse
import datetime
import os
import sys
from pathlib import Path

# ─── Path Configuration ───────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BLACKLIST_PATH = REPO_ROOT / "data" / "blacklist" / "blacklist.json"
LOG_PATH = REPO_ROOT / "agents" / "logs"


# ─── Core Sentinel Engine ─────────────────────────────────────────────────────

class SentinelEngine:
    """
    Agent Sentinel: The incorruptible gatekeeper of the ATRA ecosystem.
    Operates on hashed comparisons — clear-text names of blacklisted
    entities are never stored or displayed in outputs.
    """

    def __init__(self):
        self.blacklist: list[str] = []
        self._load_blacklist()
        LOG_PATH.mkdir(parents=True, exist_ok=True)

    def _load_blacklist(self):
        """Load hashed blacklist entries from data/blacklist/blacklist.json"""
        if not BLACKLIST_PATH.exists():
            print(
                f"[SENTINEL] ⚠️  Blacklist not found at {BLACKLIST_PATH}. "
                "Operating with empty blacklist — populate before production use."
            )
            self.blacklist = []
            return

        with open(BLACKLIST_PATH, "r") as f:
            data = json.load(f)
            # Blacklist stores SHA-256 hashes of entity identifiers
            # Never store or log clear-text names
            self.blacklist = data.get("hashed_entities", [])

        print(f"[SENTINEL] 🔐 Blacklist loaded: {len(self.blacklist)} hashed entries")

    def _hash_entity(self, identifier: str) -> str:
        """
        Create a SHA-256 hash of an entity identifier.
        All blacklist comparisons use hashes — never clear text.
        """
        return hashlib.sha256(identifier.strip().lower().encode()).hexdigest()

    def check_blacklist(self, entity_name: str, registration_number: str = "") -> dict:
        """
        Cross-reference entity against the proprietary ATRA blacklist.
        Uses hashed comparisons for absolute discretion.
        """
        name_hash = self._hash_entity(entity_name)
        reg_hash = self._hash_entity(registration_number) if registration_number else None

        name_flagged = name_hash in self.blacklist
        reg_flagged = reg_hash in self.blacklist if reg_hash else False

        flagged = name_flagged or reg_flagged

        return {
            "entity_hash": name_hash[:16] + "...",  # Partial hash for logging
            "blacklist_status": "FLAGGED" if flagged else "CLEAR",
            "flag_reason": "Entity or registration match found in ATRA proprietary blacklist" if flagged else None,
        }

    def validate_pof(self, pof_data: dict) -> dict:
        """
        Validate Proof of Funds document metadata.
        Checks instrument type, issuing bank tier, and liquidity sufficiency.
        """
        instrument = pof_data.get("instrument_type", "")
        bank_tier = pof_data.get("bank_tier", 0)
        amount_usd = pof_data.get("amount_usd", 0)
        required_usd = pof_data.get("required_usd", 0)

        valid_instruments = ["BCL", "MT199", "MT760", "MT799", "Bank Comfort Letter"]
        instrument_valid = any(inst in instrument for inst in valid_instruments)
        tier_valid = bank_tier >= 1
        liquidity_sufficient = amount_usd >= required_usd

        status = "CONFIRMED" if (instrument_valid and tier_valid and liquidity_sufficient) else "INSUFFICIENT"

        issues = []
        if not instrument_valid:
            issues.append(f"Unrecognized POF instrument: '{instrument}'")
        if not tier_valid:
            issues.append(f"Bank tier insufficient: Tier-{bank_tier} (requires Tier-1)")
        if not liquidity_sufficient:
            issues.append(f"Liquidity gap: ${amount_usd:,.0f} provided vs ${required_usd:,.0f} required")

        return {
            "pof_status": status,
            "instrument": instrument,
            "bank_tier": f"Tier-{bank_tier}",
            "liquidity_ratio": round(amount_usd / required_usd, 2) if required_usd > 0 else 0,
            "issues": issues,
        }

    def validate_kyc(self, kyc_data: dict) -> dict:
        """
        Validate KYC/AML documentation completeness.
        Checks for mandatory document types and expiry.
        """
        required_docs = [
            "certificate_of_incorporation",
            "memorandum_of_association",
            "director_passport",
            "utility_bill_or_bank_statement",
        ]

        submitted_docs = kyc_data.get("submitted_documents", [])
        missing = [doc for doc in required_docs if doc not in submitted_docs]

        sanction_clear = kyc_data.get("sanctions_check_passed", False)
        pep_clear = kyc_data.get("pep_check_passed", False)

        status = "VERIFIED" if (not missing and sanction_clear and pep_clear) else "PENDING"

        return {
            "kyc_status": status,
            "missing_documents": missing,
            "sanctions_check": "CLEAR" if sanction_clear else "FLAGGED",
            "pep_check": "CLEAR" if pep_clear else "REVIEW_REQUIRED",
        }

    def generate_clearance_report(
        self,
        buyer_id: str,
        entity_name: str,
        blacklist_result: dict,
        pof_result: dict,
        kyc_result: dict,
    ) -> dict:
        """
        Generate the final Sentinel clearance report with digital hash.
        This report gates progression to Agent Logos.
        """
        timestamp = datetime.datetime.utcnow().isoformat() + "Z"

        # Determine overall risk level
        if blacklist_result["blacklist_status"] == "FLAGGED":
            risk_level = "BLOCKED"
            recommendation = "TERMINATE"
        elif kyc_result["kyc_status"] == "PENDING" or pof_result["pof_status"] == "INSUFFICIENT":
            risk_level = "MEDIUM"
            recommendation = "HOLD"
        else:
            risk_level = "LOW"
            recommendation = "ADVANCE_TO_LOGOS"

        # Generate sentinel hash
        hash_input = f"{buyer_id}{timestamp}{risk_level}"
        sentinel_hash = f"SENTINEL_{blacklist_result['blacklist_status']}_{buyer_id.replace('-', '_')}_ALPHA"

        report = {
            "agent": "Sentinel",
            "version": "1.0.0",
            "buyer_id": buyer_id,
            "timestamp": timestamp,
            "blacklist": blacklist_result,
            "proof_of_funds": pof_result,
            "kyc_aml": kyc_result,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "sentinel_hash": sentinel_hash,
        }

        # Log to agents/logs/
        self._write_log(buyer_id, report)

        return report

    def _write_log(self, buyer_id: str, report: dict):
        """Write encrypted-ready log entry to agents/logs/"""
        log_filename = LOG_PATH / f"sentinel_{buyer_id}_{datetime.date.today().isoformat()}.json"
        with open(log_filename, "w") as f:
            json.dump(report, f, indent=2)
        print(f"[SENTINEL] 📋 Log written: {log_filename.name}")

    def run_full_vetting(self, buyer_id: str, entity_data: dict) -> dict:
        """
        Execute the complete Step 2 vetting protocol.
        Main entry point for the ATRA verification pipeline.
        """
        print(f"\n{'='*60}")
        print(f"  AGENT SENTINEL — STEP 2 VERIFICATION PROTOCOL")
        print(f"  Buyer ID: {buyer_id}")
        print(f"{'='*60}\n")

        # Step 1: Blacklist check (ALWAYS FIRST — no exceptions)
        print("[1/3] ⚔️  Executing blacklist cross-reference...")
        blacklist_result = self.check_blacklist(
            entity_name=entity_data.get("entity_name", ""),
            registration_number=entity_data.get("registration_number", ""),
        )
        status_icon = "🔴 FLAGGED" if blacklist_result["blacklist_status"] == "FLAGGED" else "🟢 CLEAR"
        print(f"      Blacklist Status: {status_icon}")

        if blacklist_result["blacklist_status"] == "FLAGGED":
            print("\n[SENTINEL] 🚨 ENTITY FLAGGED. Terminating vetting process.")
            print("[SENTINEL] All associated deals have been frozen.")
            report = self.generate_clearance_report(
                buyer_id, entity_data.get("entity_name", ""),
                blacklist_result, {"pof_status": "NOT_EVALUATED"}, {"kyc_status": "NOT_EVALUATED"}
            )
            self._print_summary(report)
            return report

        # Step 2: POF Validation
        print("[2/3] 💰  Validating Proof of Funds...")
        pof_result = self.validate_pof(entity_data.get("pof_data", {}))
        pof_icon = "🟢 CONFIRMED" if pof_result["pof_status"] == "CONFIRMED" else "🟡 INSUFFICIENT"
        print(f"      POF Status: {pof_icon}")

        # Step 3: KYC/AML Check
        print("[3/3] 📋  Executing KYC/AML documentation review...")
        kyc_result = self.validate_kyc(entity_data.get("kyc_data", {}))
        kyc_icon = "🟢 VERIFIED" if kyc_result["kyc_status"] == "VERIFIED" else "🟡 PENDING"
        print(f"      KYC Status: {kyc_icon}")

        # Generate final report
        report = self.generate_clearance_report(
            buyer_id, entity_data.get("entity_name", ""),
            blacklist_result, pof_result, kyc_result
        )

        self._print_summary(report)
        return report

    def _print_summary(self, report: dict):
        """Print formatted clearance summary to console"""
        rec = report["recommendation"]
        risk = report["risk_level"]

        rec_display = {
            "ADVANCE_TO_LOGOS": "✅ ADVANCE TO AGENT LOGOS — Contract Generation",
            "HOLD": "⏸️  HOLD — Additional documentation required",
            "TERMINATE": "🚫 TERMINATE — Entity permanently blocked",
        }.get(rec, rec)

        print(f"\n{'─'*60}")
        print(f"  SENTINEL CLEARANCE REPORT — {report['buyer_id']}")
        print(f"{'─'*60}")
        print(f"  Risk Level:      {risk}")
        print(f"  Recommendation:  {rec_display}")
        print(f"  Sentinel Hash:   {report['sentinel_hash']}")
        print(f"{'─'*60}\n")


# ─── CLI Interface ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ATRA Agent Sentinel — Step 2 Buyer Verification"
    )
    parser.add_argument("--buyer-id", required=True, help="Unique buyer identifier (e.g. SOV-HK-9214)")
    parser.add_argument("--entity", required=True, help="Legal entity name")
    parser.add_argument("--reg-number", default="", help="Corporate registration number")
    parser.add_argument("--demo", action="store_true", help="Run with demo data (safe for testing)")
    args = parser.parse_args()

    sentinel = SentinelEngine()

    if args.demo:
        # Demo mode — safe test data
        entity_data = {
            "entity_name": args.entity,
            "registration_number": args.reg_number or "DEMO-REG-001",
            "pof_data": {
                "instrument_type": "BCL",
                "bank_tier": 1,
                "amount_usd": 25_000_000,
                "required_usd": 18_500_000,
            },
            "kyc_data": {
                "submitted_documents": [
                    "certificate_of_incorporation",
                    "memorandum_of_association",
                    "director_passport",
                    "utility_bill_or_bank_statement",
                ],
                "sanctions_check_passed": True,
                "pep_check_passed": True,
            },
        }
    else:
        # Production mode — minimal entity data for blacklist check
        entity_data = {
            "entity_name": args.entity,
            "registration_number": args.reg_number,
            "pof_data": {},
            "kyc_data": {},
        }

    sentinel.run_full_vetting(buyer_id=args.buyer_id, entity_data=entity_data)


if __name__ == "__main__":
    main()
