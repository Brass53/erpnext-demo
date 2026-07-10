# ERPNext Demo – Facility- & Depotcleaning GmbH

Reproduzierbares Setup unserer ERPNext-Demo (Optimierung der Controllingprozesse).
Damit kann jede/r im Team lokal **denselben** Stand installieren.

> **Wichtig:** Dieses Repo enthält das *Rezept* + die *Demo-Daten*, **nicht** ERPNext selbst.
> ERPNext, Frappe und die deutschen Apps werden bei der Installation über `installer.py`
> anhand von `apps.json` geladen. Die Bench, `node_modules` usw. werden **nicht** eingecheckt.

---

## Inhalt des Repos

```
apps.json                     # gepinnte App-Versionen (Herzstück)
VERSIONS.md                   # exakte Commits/Branches, die bei uns laufen
backup/                       # Demo-Site-Backup (Datenbank + Dateien)
docs/                         # Runbook, Testdaten-Spezifikation, Screenshot-Template
.gitignore
README.md
```

---

## Voraussetzungen

- Docker Desktop (mind. 8 GB RAM frei; **Apple Silicon:** in Docker Desktop Rosetta aktivieren)
- VS Code + Extension „Dev Containers"
- Git

---

## Installation (Schritt für Schritt)

### 1. frappe_docker holen & Dev-Container öffnen
```bash
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp -R devcontainer-example .devcontainer
```
Dieses Repo **daneben** klonen (nicht ineinander):
```bash
git clone https://github.com/<ORG>/erpnext-demo.git
```
`erpnext-demo/apps.json` nach `frappe_docker/development/apps.json` kopieren.
Dann in VS Code den Ordner `frappe_docker` öffnen → **„Reopen in Container"**.

### 2. Installer laufen lassen (im Container-Terminal)
```bash
cd /workspace/development
# Flags mit `python installer.py -h` gegenprüfen
python installer.py -j apps.json -s development.localhost \
  -r https://github.com/frappe/frappe -t version-16 -p 3.11.9 -v
```

### 3. Apps auf der Site installieren
```bash
cd frappe-bench
source env/bin/activate
bench --site development.localhost install-app erpnext
bench --site development.localhost install-app eu_einvoice
bench --site development.localhost install-app erpnext_datev
bench --site development.localhost add-to-hosts
```

### 4. Demo-Zustand herstellen (Backup einspielen)
Das Backup aus `erpnext-demo/backup/` nach
`frappe-bench/sites/development.localhost/private/backups/` kopieren, dann:
```bash
bench --site development.localhost restore <pfad-zur-database.sql.gz> \
  --with-public-files <public-files.tar> \
  --with-private-files <private-files.tar>
bench --site development.localhost migrate
```
> Restore überschreibt die Site-Daten mit unserem Demo-Zustand (Company, Kunden,
> Artikel, Rechnungen, Dunning Type, Bankkonto).

### 5. Starten
```bash
bench use development.localhost
bench start
```
Browser: **http://development.localhost:8000** (Administrator / admin)

---

## Alternative zu Schritt 4: Daten per Import statt Backup

Wenn ihr die Demo-Daten lieber frisch importieren wollt (z. B. weil sich Werte ändern),
liegen die CSVs unter `docs/`/`demo-data/` und werden über
**Datenimport** (Data Import Tool) in ERPNext eingespielt. Reihenfolge:
Company-Setup (SKR04, 19 % USt) → Kunden → Artikel → Rechnungen → Bank-CSV → Dunning Type.
Details in `docs/Testdaten-Spezifikation`.

---

## Troubleshooting

- **`redis-server: not found`** → tritt bei manuellem `bench init` auf. Immer `installer.py` nutzen (Redis läuft in eigenen Containern).
- **Build bricht mit `pypika`-Fehler** → Python 3.14 / neue uv-Bench. Fix: in `.devcontainer/docker-compose.yml` Bench-Image pinnen (z. B. `frappe/bench:v5.27.0`) und Installer mit `-p 3.11.9`.
- **„version-16 existiert nicht"** → das ist ein **App-Branch** (in `apps.json` / per `-t`), nicht das frappe_docker-Repo (immer `main`).
- **Encrypted-Fields nach Restore leer** → nur relevant, wenn verschlüsselte Felder (z. B. E-Mail-Passwörter) genutzt werden. Für die reine Demo ignorierbar.

---

## Versionen

Siehe `VERSIONS.md` für die exakten Commits. Branches bewegen sich – wer 1:1 unseren
Stand will, checkt die dort notierten Commit-Hashes aus.
