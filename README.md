# 🌍 ATRA Sovereign Trade Engine

> *"Connecting African Resources to Global Markets through Integrity, Transparency, and Scale."*

**The Digital Gateway to West African Wealth**

---

## Executive Mission

The **ATRA Sovereign Trade Engine** is an institutional-grade, AI-integrated platform that facilitates international commodity trade — connecting verified global buyers with West African resource suppliers across **Precious Metals**, **Energy**, and **Agri-Commodities**.

Headquartered in Nouakchott, Mauritania, ATRA operates as a trusted principal intermediary with deep operational reach into the **West African Gold Belt** (Mauritania · Mali · Burkina Faso).

---

## Core Value Propositions

| Pillar | Description |
|--------|-------------|
| **The Trust Bridge** | A rigorous 6-step transaction framework: Consultation → Verification → Negotiation → Documentation → Payment → Logistics |
| **Green Gold Protocol** | ESG mandate transitioning artisanal miners in Mali/Burkina Faso to mercury-free production — verified, certified, institutional-grade |
| **Institutional Scale** | Proven 1–5 MT monthly gold pipeline with Tier-1 offtake infrastructure |
| **Dual-Stream Settlement** | Traditional (LC/Escrow/Bank Guarantee) + Digital (USDT ERC-20/TRC-20, BTC) — simultaneous support |
| **Intelligence Moat** | Proprietary Industry Blacklist and 6-step vetting that eliminates ghost brokers and bad-faith actors |

---

## Autonomous Agent Architecture

Five specialized AI agents manage the full transaction lifecycle. Each agent has exactly **7 core skills** to ensure operational precision.

| Agent | Designation | Primary Mandate | Status |
|-------|-------------|-----------------|--------|
| **Sentinel** | Risk & Vetting | Industry Blacklist management, Step 2 verification, KYC/AML | 🟢 Online |
| **Alchemist** | Purity & ESG | Green Gold Protocol audits, commodity spec, assay coordination | 🟢 Online |
| **Logos** | Contractual | NCNDA, SPA, Agency Agreements, commission protection | 🟢 Online |
| **Vault** | Settlement | Trad-Fi + USDT/BTC dual-stream execution | 🟢 Online |
| **Navigator** | Logistics | Sea-to-shelf coordination via Port of Nouakchott | 🟢 Online |

Agent configs: [`agents/configs/`](agents/configs/)

---

## Repository Structure

```
atra-trade-engine/
├── .github/workflows/          # CI/CD and automated vetting pipelines
├── agents/
│   ├── configs/                # Agent personality & skills (.md files)
│   ├── logic/                  # Python implementations of agent skills
│   └── logs/                   # Daily Intelligence Reports (gitignored)
├── backend/
│   ├── api/                    # FastAPI endpoints (portal + mobile)
│   ├── core/                   # Blacklist logic, Step 2 vetting engine
│   ├── database/               # Allocation and partner vetting schema
│   └── secure_vault/           # Encrypted document storage (gitignored)
├── frontend/
│   ├── portal/                 # Sovereign Client Dashboard (Next.js)
│   ├── mobile/                 # Internal War Room App (React Native)
│   └── public/                 # Brand assets (Neo-African Gold palette)
├── data/
│   ├── blacklist/              # SHA-256 hashed bad-actor database
│   └── markets/                # Commodity pricing and ESG reference data
├── docs/
│   ├── brand/                  # Visual identity and design standards
│   ├── legal/                  # NCNDA, SPA, Agency Agreement templates
│   └── strategy/               # Master business plan and funnel architecture
├── scripts/
│   ├── run_sentinel.py         # Daily vetting trigger script
│   └── deploy_portal.sh        # Sovereign Portal deployment
├── tests/                      # Unit tests for vetting and settlement logic
├── .env.example                # Environment variable template
├── .gitignore
├── CONTRIBUTING.md
├── README.md
└── requirements.txt
```

---

## Technical Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+ / FastAPI |
| **Frontend** | Next.js 14 / Tailwind CSS (Neo-African Gold aesthetic) |
| **Mobile** | React Native (Internal War Room App) |
| **Intelligence** | Agent configs fed to LLM layer (Claude / GPT-4o) |
| **Database** | PostgreSQL (allocations) + Redis (session/blacklist cache) |
| **Settlement** | TradFi: SWIFT MT700/MT760/MT103 · Digital: USDT (ERC-20/TRC-20), BTC |

---

## Getting Started

### Prerequisites
```bash
python 3.11+
node 18+
git
```

### Setup
```bash
git clone https://github.com/MajorDream444/ATRA.git
cd ATRA
cp .env.example .env
pip install -r requirements.txt
```

### Run Sentinel Vetting (Demo Mode)
```bash
python backend/core/sentinel_vetting.py \
  --buyer-id SOV-HK-9214 \
  --entity "Test Institutional Partner" \
  --demo
```

### Initialize Perimeter Security
```bash
python scripts/run_sentinel.py
```

### Deploy Sovereign Portal
```bash
bash scripts/deploy_portal.sh
```

---

## The 6-Step Secure-Close Framework

```
Step 1: CONSULTATION
  └─ Buyer inquiry received via Sovereign Portal
  └─ Agent Sentinel: Initial traffic screening

Step 2: VERIFICATION
  └─ KYC / AML documentation review
  └─ Proof of Funds (BCL / MT199 / MT760) validation
  └─ Proprietary Blacklist cross-reference
  └─ Digital footprint analysis
  └─ → Sentinel clearance hash issued

Step 3: NEGOTIATION
  └─ Agent Alchemist: Purity and ESG stream selection
  └─ Pricing: LBMA Second London Fixing mechanism
  └─ Volume and duration agreement

Step 4: DOCUMENTATION
  └─ Agent Logos: NCNDA generation
  └─ Agent Logos: SPA drafting (with Green Gold addendum if applicable)
  └─ Agent Logos: Commission protection and agency agreement
  └─ Digital signature lifecycle management

Step 5: PAYMENT & SECURITY
  └─ Agent Vault: DLC / MT700 instructions issued
  └─ Agent Vault: USDT/BTC wallet address whitelisted and provided
  └─ Commission payout automation armed

Step 6: LOGISTICS & CLOSING
  └─ Agent Navigator: Armored convoy from mine to Nouakchott
  └─ Agent Navigator: Customs pre-clearance at PANPA
  └─ Agent Navigator: GPS-tracked sovereign container shipping
  └─ Agent Navigator: Final assay + Proof of Shipment (POS)
  └─ Agent Vault: Settlement released upon POS confirmation
```

---

## AI Contributor Instructions

> **Attention: Claude Code, Antigravity, and all AI collaborators**

This repository manages the facilitation of high-value West African resource transactions. When contributing code or content:

1. **Always prioritize the Blacklist check** before any Step 2 logic — no exceptions
2. **Include the Green Gold Protocol hook** in all Gold-related functions
3. **Never bypass Agent Vault's security checks** in settlement logic
4. **Discretion is absolute** — never log clear-text entity names to console or public files
5. **Dual-stream settlement** (Trad-Fi + Digital) must be supported simultaneously
6. **Commission protection clauses are non-negotiable** — never alter them in templates
7. **Port of Nouakchott is the primary logistics hub** — all navigation logic defaults here

Review `CONTRIBUTING.md` before any pull request.

---

## Security & Confidentiality

- All client identities and transaction details are protected under international NCNDA standards
- `backend/secure_vault/` contains sensitive documents — **never commit this directory**
- `data/blacklist/` uses SHA-256 hashed entity identifiers — clear-text names are never stored
- Wallet private keys and seed phrases go in `.env` only — never in code

---

## Contact

**Principal:** M. Diallo
**Email:** m.diallo@atrasarl.com
**Phone:** +222-44290990 | +222-41745940
**Web:** [www.atrasarl.com](https://www.atrasarl.com)

---

*ATRA Sovereign Trade Engine — Version 1.0.0 · March 2026*
