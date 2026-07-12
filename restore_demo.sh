#!/usr/bin/env bash
#
# restore_demo.sh – setzt die ERPNext-Site development.localhost in EINEM Befehl
# auf unseren vollständigen Demo-Stand zurück.
#
# Enthalten in diesem Backup (Superset des Kollegen-Backups):
#   - Company (SKR04, 19 % USt), 2 Kunden, 2 Artikel, Steuervorlage, Bankkonto
#   - Rechnung RE-2026-0001 -> Paid (inkl. Bank-Import + Zahlungsabgleich, Prozess 2)
#   - Rechnung RE-2026-0002 -> Overdue
#   - Mahnung DUNN-07-26-00001 (Prozess 3, echtes Mahn-Dokument)
#   - Übungs-Entwürfe fürs Live-Vorführen:
#       * TS-2026-00003 (Timesheet, Entwurf)  -> Schritt 6/7
#       * RE-2026-0003  (Rechnung, Entwurf)   -> Schritt 8 (XRechnung)
#
# Voraussetzung: der frappe_docker-Dev-Container läuft.
# Aufruf vor/nach einer Demo einfach:   ./restore_demo.sh
#
set -euo pipefail

# Container-Name des laufenden frappe_docker-Dev-Containers.
# Bei Bedarf überschreiben:  CONTAINER=<name> ./restore_demo.sh
CONTAINER="${CONTAINER:-frappe_docker_devcontainer-frappe-1}"
SITE="development.localhost"
DB_ROOT_PW="${DB_ROOT_PW:-123}"          # Standard-Passwort des Dev-Containers
STAMP="20260712_144126-development_localhost"

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
  echo "        (oder anderen Namen setzen:  CONTAINER=<name> ./restore_demo.sh )" >&2
  exit 1
fi

echo ">> Kopiere Backup in den Container ..."
docker cp "$DB"   "$CONTAINER:/tmp/$(basename "$DB")"
docker cp "$PUB"  "$CONTAINER:/tmp/$(basename "$PUB")"
docker cp "$PRIV" "$CONTAINER:/tmp/$(basename "$PRIV")"

echo ">> Stelle Site '$SITE' auf den Demo-Stand wieder her ..."
docker exec "$CONTAINER" bash -c "cd /workspace/development/frappe-bench && \
  bench --site $SITE restore /tmp/$(basename "$DB") \
    --with-public-files  /tmp/$(basename "$PUB") \
    --with-private-files /tmp/$(basename "$PRIV") \
    --force --mariadb-root-password $DB_ROOT_PW"

echo ">> Fertig. Site '$SITE' ist auf dem vollständigen Demo-Stand (inkl. Übungs-Entwürfe)."
