#!/usr/bin/env python3
"""
ATRA Sovereign Trade Engine
scripts/hash_entity.py — Secure Blacklist Entry Utility

Safely adds entity identifiers to the ATRA proprietary blacklist
by converting them to SHA-256 hashes. Clear-text names are NEVER
stored — only hashes are written to the blacklist database.

Usage:
    python scripts/hash_entity.py --entity "Entity Name" --reg "REG-NUMBER"
    python scripts/hash_entity.py --entity "Entity Name" --dry-run
"""

import hashlib
import json
import argparse
import datetime
import getpass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLACKLIST_PATH = ROOT / "data" / "blacklist" / "blacklist.json"


def hash_identifier(identifier: str) -> str:
    return hashlib.sha256(identifier.strip().lower().encode()).hexdigest()


def add_to_blacklist(entity_name: str, reg_number: str = "", dry_run: bool = False):
    name_hash = hash_identifier(entity_name)
    reg_hash = hash_identifier(reg_number) if reg_number else None

    print(f"\n  ATRA BLACKLIST ENTRY UTILITY")
    print(f"  {'─' * 50}")
    print(f"  Entity Hash:  {name_hash[:32]}...")
    if reg_hash:
        print(f"  Reg Hash:     {reg_hash[:32]}...")

    if dry_run:
        print(f"\n  [DRY RUN] — No changes written to blacklist.")
        print(f"  To commit, run without --dry-run flag.")
        return

    # Confirm before writing
    confirm = input(f"\n  ⚠️  Add these hashes to the ATRA blacklist? [yes/no]: ").strip().lower()
    if confirm != "yes":
        print("  Aborted. No changes made.")
        return

    # Load existing blacklist
    with open(BLACKLIST_PATH, "r") as f:
        data = json.load(f)

    existing = data.get("hashed_entities", [])

    added = []
    if name_hash not in existing:
        existing.append(name_hash)
        added.append("entity_name")
    if reg_hash and reg_hash not in existing:
        existing.append(reg_hash)
        added.append("registration_number")

    if not added:
        print("  Entity already exists in blacklist. No changes made.")
        return

    # Remove placeholder if present
    placeholder = "PLACEHOLDER_REPLACE_WITH_SHA256_HASH_OF_ENTITY_NAME"
    if placeholder in existing:
        existing.remove(placeholder)

    data["hashed_entities"] = existing
    data["_metadata"]["total_entries"] = len([e for e in existing if len(e) == 64])
    data["_metadata"]["last_updated"] = datetime.date.today().isoformat()

    with open(BLACKLIST_PATH, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n  ✅ Blacklist updated.")
    print(f"  Fields added: {', '.join(added)}")
    print(f"  Total entries: {data['_metadata']['total_entries']}")
    print(f"\n  SECURITY: The clear-text entity name was never written to disk.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ATRA Blacklist Entry Utility")
    parser.add_argument("--entity", required=True, help="Legal entity name to blacklist")
    parser.add_argument("--reg", default="", help="Corporate registration number")
    parser.add_argument("--dry-run", action="store_true", help="Preview hash without writing")
    args = parser.parse_args()

    add_to_blacklist(
        entity_name=args.entity,
        reg_number=args.reg,
        dry_run=args.dry_run,
    )
