#!/usr/bin/env bash
#
# restore_demo_live.sh – Startpunkt für die LIVE-Demo der interaktiven Schritte.
#
# Setzt die Site auf einen Demo-Startpunkt, der live vorführbar ist:
#   - Ein-Klick-Auto-Reconcile bereit: 2 Bank-Zeilen (unabgeglichen) + Zahlung
#     mit Referenz "RE-2026-0001" liegen vor. Bank Reconciliation Tool ->
#     "Auto Reconcile" ordnet die Zeile mit der Rechnungsnummer AUTOMATISCH zu;
#     die 250-EUR-Zeile ohne Referenz bleibt offen.
#   - Übungs-Entwürfe TS-2026-00003 / RE-2026-0003       -> Schritt 6/7/8 live zeigen
#   - RE-2026-0002 (Overdue) + Dunning Type              -> Schritt 10 (Create -> Dunning)
#   - DATEV Settings vorhanden                           -> Schritt 11 (DATEV-Export)
#   - Konto-Fixes (Forderung 1200 / Bank 1800) enthalten
#
# Demo-Reihenfolge:
#   Schritt 7  : aus TS-2026-00003 -> Rechnung erstellen (Create Sales Invoice)
#   Schritt 8  : Entwurf RE-2026-0003 submitten -> XRechnung (Download eInvoice)
#   Schritt 9  : Bank Reconciliation Tool -> "Auto Reconcile" (automatische Zuordnung)
#   Schritt 10 : RE-2026-0002 -> Create -> Dunning
#   Schritt 11 : DATEV-Report -> Download DATEV File
#
# Der FERTIGE Endstand liegt weiterhin in  restore_demo.sh.
#
set -euo pipefail

CONTAINER="${CONTAINER:-frappe_docker_devcontainer-frappe-1}"
SITE="development.localhost"
DB_ROOT_PW="${DB_ROOT_PW:-123}"
STAMP="20260730_221809-development_localhost"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BK_DIR="$SCRIPT_DIR/backup"
DB="$BK_DIR/${STAMP}-database.sql.gz"
PUB="$BK_DIR/${STAMP}-files.tar"
PRIV="$BK_DIR/${STAMP}-private-files.tar"

for f in "$DB" "$PUB" "$PRIV"; do
  [ -f "$f" ] || { echo "FEHLER: Backup-Datei fehlt: $f" >&2; exit 1; }
done
if ! docker inspect "$CONTAINER" >/dev/null 2>&1; then
  echo "FEHLER: Container '$CONTAINER' läuft nicht. Erst den Dev-Container starten." >&2
  exit 1
fi

echo ">> Kopiere live-start-Backup in den Container ..."
docker cp "$DB"   "$CONTAINER:/tmp/$(basename "$DB")"
docker cp "$PUB"  "$CONTAINER:/tmp/$(basename "$PUB")"
docker cp "$PRIV" "$CONTAINER:/tmp/$(basename "$PRIV")"

echo ">> Stelle Site '$SITE' auf den LIVE-Startpunkt her ..."
docker exec "$CONTAINER" bash -c "cd /workspace/development/frappe-bench && \
  bench --site $SITE restore /tmp/$(basename "$DB") \
    --with-public-files  /tmp/$(basename "$PUB") \
    --with-private-files /tmp/$(basename "$PRIV") \
    --force --mariadb-root-password $DB_ROOT_PW"

echo ">> Fertig. RE-2026-0001 ist offen – jetzt Schritt 7-10 live vorführbar."
