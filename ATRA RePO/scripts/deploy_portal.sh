#!/usr/bin/env bash
# ATRA Sovereign Trade Engine — Portal Deployment Script
# Usage: bash scripts/deploy_portal.sh [environment]

set -e

ENV=${1:-"development"}
PORTAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/frontend/portal"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ATRA SOVEREIGN PORTAL — DEPLOYMENT                  ║"
echo "║  Environment: ${ENV}                                  "
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Verify portal exists
if [ ! -f "$PORTAL_DIR/index.html" ]; then
    echo "❌ Portal not found at $PORTAL_DIR"
    exit 1
fi

echo "✅ Portal source verified: $PORTAL_DIR"

if [ "$ENV" = "development" ]; then
    echo ""
    echo "  Starting local development server..."
    echo "  Portal will be available at: http://localhost:3000"
    echo ""
    cd "$PORTAL_DIR"
    python3 -m http.server 3000
elif [ "$ENV" = "production" ]; then
    echo ""
    echo "  Production deployment requires:"
    echo "  1. A configured server with HTTPS (SSL/TLS)"
    echo "  2. Nginx or Caddy as reverse proxy"
    echo "  3. Valid domain and DNS configured"
    echo ""
    echo "  Next.js build (from frontend/portal/):"
    echo "    npm install && npm run build && npm start"
    echo ""
    echo "  For static hosting (HTML only):"
    echo "    Copy frontend/portal/index.html to your web server root"
    echo ""
fi

echo ""
echo "  SENTINEL NOTE: Ensure .env is configured before"
echo "  connecting the portal to the backend API."
echo ""
