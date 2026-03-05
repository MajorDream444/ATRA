# CONTRIBUTING.md — ATRA Sovereign Trade Engine

## 1. Core Philosophy: The Trust Bridge

Every contribution to this repository must reinforce ATRA's position as a professional, secure, and transparent intermediary. We do not just move commodities; we manage risk, reputation, and relationships.

**Absolute Principles:**

- **Discretion is Non-Negotiable.** Under no circumstances shall partner identities, specific offtake volumes, or Blacklist entity names be logged to public consoles or exported from the secure environment.
- **Process Integrity.** Code must strictly follow the 6-Step Transaction Framework: Consultation → Verification → Negotiation → Documentation → Payment → Logistics.
- **Sovereign-Grade Quality.** If your code would embarrass a private bank, do not submit it.

---

## 2. Agent-Specific Coding Standards

### Agent Sentinel (Vetting & Risk)
- **Mandate:** Logic must prioritize the Blacklist check before any other Step 2 action.
- **Constraint:** Never cache POF or KYC documents in unencrypted temporary directories.
- **Constraint:** All blacklist comparisons must use SHA-256 hashed identifiers — clear-text names never appear in code or UI.

### Agent Alchemist (ESG & Purity)
- **Mandate:** All Gold-related functions must include a hook for the Green Gold Protocol.
- **Constraint:** Market price data must be sourced only from LBMA or designated agency mechanisms.
- **Constraint:** ESG certificates are never issued without physical verification data.

### Agent Logos (Contractual)
- **Mandate:** NCNDA and commission protection clauses are non-negotiable — never alter them to reduce protection.
- **Constraint:** No SPA is generated without a confirmed Sentinel clearance hash.
- **Constraint:** All archived documents in `backend/secure_vault/` must be encrypted before storage.

### Agent Vault (Settlement)
- **Mandate:** Settlement logic must always support both Traditional (LC/Escrow) and Digital (USDT/BTC) streams simultaneously.
- **Constraint:** No transaction is marked "Complete" without Agent Navigator's final delivery hash.
- **Constraint:** Wallet addresses, private keys, and seed phrases never appear in source code — use `.env` only.

### Agent Navigator (Logistics)
- **Mandate:** Port of Nouakchott is the primary logistics hub — all routing logic defaults here unless explicitly specified otherwise.
- **Constraint:** Proof of Shipment (POS) is never issued without independent assay confirmation.
- **Constraint:** Vault settlement release is triggered only by confirmed, GPS-verified delivery — never estimated.

---

## 3. Data Handling & Security Protocols

### `backend/secure_vault/` Directory
- For local simulation and testing of partner documentation only.
- **AI Directive:** Never suggest code that moves files from `secure_vault/` to any cloud storage without 256-bit encryption.
- This directory is in `.gitignore` — it must never be committed.

### `data/blacklist/blacklist.json`
- Contains SHA-256 hashes only — no clear-text entity names.
- **AI Directive:** Logic interacting with the blacklist must use hashed comparison functions only.
- Read access: Sentinel Agent. Write access: ATRA Principal only.
- To add an entry, use: `python scripts/hash_entity.py --entity "Name" --reg "REG-NUM"`

### `agents/logs/`
- Daily Intelligence Reports are stored here.
- This directory is gitignored — logs are never committed to version control.

---

## 4. Development Workflow

1. **Branch Naming:** Use the 6-step naming convention:
   - `feat/step2-kyc-validation`
   - `feat/step5-usdt-settlement`
   - `fix/step6-navigator-customs`
   - `docs/agent-alchemist-esg-protocol`

2. **Local Initialization:**
   ```bash
   python scripts/run_sentinel.py  # Verify local security perimeter
   ```

3. **Testing:** All PRs must include unit tests in `tests/`. Settlement logic and blacklist checks require 100% test coverage.

4. **PR Review:** Pull Requests that alter `docs/legal/` templates (NCNDA, SPA, commission agreements) require explicit approval from ATRA Principal before merge.

---

## 5. Visual Standards (Neo-African Gold Aesthetic)

All UI contributions to the Sovereign Portal (`frontend/portal/`) or the Internal War Room App (`frontend/mobile/`) must adhere to:

| Element | Standard |
|---------|----------|
| **Primary Color** | `#C9A84C` (Matte Gold) |
| **Background** | `#0D0D0F` (Deep Charcoal) |
| **Accent** | `#2ECC71` (Sentinel Green — verified/clear) |
| **Alert** | `#E74C3C` (Vault Red — flagged/blocked) |
| **Typography** | Cormorant Garamond (serif) + Space Mono (mono) + Rajdhani (display) |
| **Aesthetic** | Cyber-Industrial · Neo-African Excellence · Institutional Authority |

No stock photography. No generic gradients. No "startup" aesthetics.

---

## 6. What ATRA Is — and Is Not

**ATRA IS:**
- A professional commodity brokerage and trade facilitation firm
- A trusted intermediary connecting verified buyers with verified African suppliers
- An ESG leader via the Green Gold Protocol
- A dual-stream settlement innovator (TradFi + Digital)

**ATRA IS NOT:**
- A direct mine owner or commodity title holder
- A financial services provider or money transmitter
- A speculative trading desk
- A public marketplace

All code must reflect this distinction.

---

## Final Instruction for AI Agents

You are a collaborator in a high-value international trade agency serving institutional buyers and sovereign-level counterparties. Your primary goal is to facilitate international business by linking global demand with reliable African supply sources while ensuring total compliance, absolute discretion, and smooth execution.

Write code that would make a Swiss private banker and a Mauritanian mine operator equally confident.

---

*"The deal exists in principle. Code makes it sovereign."*
