#!/usr/bin/env bash
#
# restore_demo_live.sh – Startpunkt für die LIVE-Demo der interaktiven Schritte.
#
# Setzt die Site auf den Stand VOR den interaktiven Prozessen, sodass du sie
# live vorführen kannst:
#   - RE-2026-0001 = Unpaid/offen (noch NICHT bezahlt)   -> Schritt 9 abgleichbar
#   - KEINE Bank-Transaktionen, keine Zahlung            -> Bank-Import live zeigen
#   - KEINE Mahnung (Dunning Type bleibt)                -> Schritt 10 live zeigen
#   - Übungs-Entwürfe TS-2026-00003 / RE-2026-0003       -> Schritt 6/7/8 live zeigen
#   - Stammdaten, RE-2026-0002 (Overdue) usw. vorhanden
#
# Damit ist die Reihenfolge in der Demo:
#   Schritt 7  : aus TS-2026-00003 -> Rechnung erstellen (Create Sales Invoice)
#   Schritt 8  : Entwurf RE-2026-0003 submitten -> XRechnung (Download eInvoice)
#   Schritt 9  : bank_import CSV importieren -> Bank Reconciliation -> A wird Paid
#   Schritt 10 : Dunning anlegen -> Fetch Overdue Payments (RE-2026-0002)
#
# Der FERTIGE Endstand liegt weiterhin in  restore_demo.sh.
#
set -euo pipefail

CONTAINER="${CONTAINER:-frappe_docker_devcontainer-frappe-1}"
SITE="development.localhost"
DB_ROOT_PW="${DB_ROOT_PW:-123}"
STAMP="20260712_112006-development_localhost"

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
