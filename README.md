# ERPNext Demo – Facility- & Depotcleaning GmbH

Reproduzierbares Setup unserer ERPNext-Demo (Projekt „Optimierung der Controllingprozesse").
Damit installiert **jede/r im Team – und der Prof – lokal denselben Stand**.

> Dieses Repo enthält das **Rezept** (`apps.json`, diese Anleitung) + die **Demo-Daten**
> (`backup/`), **nicht** ERPNext selbst. ERPNext, Frappe und die deutschen Apps werden bei
> der Installation über `installer.py` anhand von `apps.json` geladen. Die Bench,
> `node_modules` usw. werden bewusst **nicht** eingecheckt (siehe `.gitignore`).

---

> ## ⚠️ Wichtige Korrektur (2026-07-10): Python 3.14 + Node 24 nötig
>
> Die frühere Anleitung mit **Python 3.11.9** funktioniert **nicht** mehr: Die aktuelle
> `version-16` von Frappe/ERPNext verlangt **Python ≥ 3.14** *und* **Node ≥ 24**. Der
> zusätzliche Schritt dazu steht unten als **Schritt 1a**. Das mitgelieferte Backup enthält
> inzwischen den **vollständigen Demo-Datensatz** (2 Kunden, 2 Artikel, Rechnungen
> RE-2026-0001 = *Paid* und RE-2026-0002 = *Overdue*, Zahlung, Timesheet, Mahn-Typ).

## ⏱️ TL;DR für den Prof (Kurzfassung)

Voraussetzung: **Docker Desktop**, **VS Code + Extension „Dev Containers"**, **Git**.

```bash
# 1) Offizielles Docker-Rezept holen und Dev-Container-Konfig aktivieren
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp -R devcontainer-example .devcontainer

# 2) Dieses Repo DANEBEN klonen (nicht ineinander)
cd ..
git clone <REPO-URL> erpnext-demo

# 3) Unsere App-Liste + Backup in den Container-sichtbaren Ordner kopieren
cp erpnext-demo/apps.json        frappe_docker/development/apps.json
cp -R erpnext-demo/backup        frappe_docker/development/backup

# 4) WICHTIG (sonst Build-Fehler): Bench-Image pinnen
#    In frappe_docker/.devcontainer/docker-compose.yml die Zeile mit "image: frappe/bench:..."
#    auf  image: frappe/bench:v5.27.0  setzen.
```

Dann `frappe_docker` in VS Code öffnen → **„Reopen in Container"** → im Container-Terminal
die Blöcke aus **Schritt 2–5** unten ausführen. Login am Ende:
**http://development.localhost:8000** — Administrator / `admin`.

Wer nur *durchklicken* will, findet den fachlichen Ablauf in
`docs/Testdaten-und-Einpflege-Anleitung.md`.

---

## Inhalt des Repos

```
apps.json                     # gepinnte App-Versionen (Herzstück der Installation)
VERSIONS.md                   # exakte Versionen/Commits, die bei uns laufen
backup/                       # Demo-Site-Backup (DB + öffentliche + private Dateien)
  ├─ ...-database.sql.gz
  ├─ ...-files.tar
  └─ ...-private-files.tar
docs/
  ├─ Testdaten-Spezifikation.pdf            # was die Demo an Daten braucht
  ├─ Testdaten-und-Einpflege-Anleitung.md   # konkreter Datensatz + Klick-Anleitung
  └─ bank_import.csv                         # fertige Bank-CSV für Prozess 2
.gitignore
README.md                     # diese Datei
```

---

## Voraussetzungen

- **Docker Desktop** (mind. 8 GB RAM frei; **Apple Silicon/M-Chip:** in Docker Desktop unter
  *Settings → General* „Rosetta" aktivieren)
- **VS Code** + Extension **„Dev Containers"** (`ms-vscode-remote.remote-containers`)
- **Git**

Kein Python, Node, Redis oder MariaDB auf dem Rechner nötig – das läuft alles in Containern.

---

## Installation – Schritt für Schritt

### Schritt 0: Repos holen und vorbereiten (auf dem Host, nicht im Container)

```bash
# offizielles frappe_docker
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
cp -R devcontainer-example .devcontainer

# dieses Repo daneben (NICHT in frappe_docker hinein) klonen
cd ..
git clone <REPO-URL> erpnext-demo

# unsere App-Liste an die vom Container erwartete Stelle kopieren
cp erpnext-demo/apps.json frappe_docker/development/apps.json

# Backup an eine im Container sichtbare Stelle kopieren
# (alles unter frappe_docker/development/ ist im Container als /workspace/development/ da)
cp -R erpnext-demo/backup frappe_docker/development/backup
```

**Bench-Image pinnen (verhindert den häufigsten Build-Fehler):**
In `frappe_docker/.devcontainer/docker-compose.yml` die Zeile mit dem Bench-Image
(≈ Zeile 45) auf eine feste Version setzen:

```yaml
    image: frappe/bench:v5.27.0
```

Hintergrund: Wir pinnen das Image, damit alle denselben Ausgangsstand haben. **Achtung:**
v5.27.0 bringt nur Python 3.11 / Node 20 mit – die aktuelle `version-16` braucht aber
**Python ≥ 3.14** und **Node ≥ 24**. Die installieren wir in **Schritt 1a** im Container nach.

Jetzt in VS Code den Ordner **`frappe_docker`** öffnen und unten rechts
**„Reopen in Container"** klicken (oder `Strg/Cmd+Shift+P` → „Dev Containers: Rebuild and
Reopen in Container"). Der erste Build dauert einige Minuten.

> Ab hier laufen **alle** Befehle **im Container-Terminal** (VS Code: `Strg+Shift+ö`/`` Ctrl+Shift+` ``).
> Der Prompt sollte auf `frappe@…:/workspace/development$` stehen.

### Schritt 1a: Python 3.14 + Node 24 im Container bereitstellen (WICHTIG, neu)

Das gepinnte Bench-Image `v5.27.0` bringt nur Python 3.11 / Node 20 mit – die aktuelle
`version-16` verlangt aber **Python ≥ 3.14** und **Node ≥ 24**. Ohne diesen Schritt bricht
`bench init` ab (Python: `SyntaxError`; Node: `yarn`-Engine-Fehler). Einmalig im Container:

```bash
pyenv install -s 3.14.2                    # Python 3.14 bauen (dauert ein paar Minuten)
nvm install 24 && nvm alias default 24     # Node 24 als Standard setzen
npm install -g yarn                        # yarn hängt an der Node-Version → für Node 24 neu
```

### Schritt 1: Installer laufen lassen (Bench + Apps + frische Site)

```bash
cd /workspace/development
# Flags kann man mit  python installer.py -h  einsehen
python installer.py -j apps.json -s development.localhost \
  -r https://github.com/frappe/frappe -t version-16 -p 3.14.2 -n 24 -v
```

Das legt die `frappe-bench/` an, holt Frappe + die Apps aus `apps.json` und erstellt die
Site `development.localhost`.

### Schritt 2: Sicherstellen, dass die Apps auf der Site installiert sind

```bash
cd frappe-bench
source env/bin/activate

bench --site development.localhost install-app erpnext
bench --site development.localhost install-app eu_einvoice
bench --site development.localhost install-app erpnext_datev
bench --site development.localhost add-to-hosts
```

> Meldet ein Befehl „App … is already installed", ist das in Ordnung – einfach weiter.
> (Der Datenstand kommt ohnehin gleich aus dem Backup.)

### Schritt 3: Demo-Zustand herstellen (unser Backup einspielen)

Die Backup-Dateien liegen im Container unter `/workspace/development/backup/`.
Aus dem Ordner `frappe-bench`:

```bash
BK=/workspace/development/backup
bench --site development.localhost restore \
  $BK/20260710_224015-development_localhost-database.sql.gz \
  --with-public-files  $BK/20260710_224015-development_localhost-files.tar \
  --with-private-files $BK/20260710_224015-development_localhost-private-files.tar

bench --site development.localhost migrate
```

> `restore` **überschreibt** die frische Site mit unserem Demo-Zustand (Company, Kunden,
> Artikel, Rechnungen, Dunning Type, Bankkonto). `migrate` bringt das DB-Schema auf den
> Stand der installierten App-Versionen.

Falls das Admin-Passwort aus dem Backup abweicht, zurücksetzen:

```bash
bench --site development.localhost set-admin-password admin
```

### Schritt 4: Starten

```bash
bench use development.localhost
bench start
```

Browser öffnen: **http://development.localhost:8000**
Login: **Administrator** / **admin**

---

## Alternative: Demo-Daten frisch eintragen statt Backup einspielen

Wenn ihr die Werte lieber selbst eingebt (z. B. weil sich etwas ändern soll), lasst
**Schritt 3 weg** und pflegt den Datensatz nach der fachlichen Anleitung ein:
`docs/Testdaten-und-Einpflege-Anleitung.md` (enthält den fertigen, in sich konsistenten
Datensatz, die Reihenfolge und die Bank-CSV `docs/bank_import.csv`).
Reihenfolge in Kurzform: Company-Setup (SKR04, 19 % USt) → Payment Terms → Kunden →
Artikel → Timesheet → Rechnungen → Bank-Import → Dunning Type.

**Schneller: per Skript.** `scripts/seed_demo.py` legt genau diesen Datensatz automatisch an
(idempotent, mehrfach ausführbar) – Kunden, Artikel, beide Rechnungen (RE-2026-0001 = Paid,
RE-2026-0002 = Overdue), Zahlung, Timesheet, Steuervorlage 19 %, Bankkonto und Dunning Type.
Im Container ausführen (Datei vorher wie das Backup nach `frappe_docker/development/` kopieren):

```bash
echo "exec(open('/workspace/development/seed_demo.py').read(), globals())" \
  | bench --site development.localhost console
```

Noch **nicht** enthalten (rein interaktiv, fürs Live-Demo): der Bank-Import aus
`docs/bank_import.csv` (Prozess 2, inkl. der bewusst unzuordenbaren 250-€-Zeile) und das
Mahn-*Dokument* (Prozess 3, „Fetch Overdue Payments" – der Dunning Type steht bereit).

---

## Verifizieren, dass es läuft (kurze Abnahme)

> ✅ **Backup ist vollständig:** Das mitgelieferte Backup (`20260710_224015-…`) enthält den
> kompletten Demo-Datensatz. Nach Restore + `migrate` ist die folgende Abnahme-Liste erfüllt.

Nach dem Login sollte sichtbar sein:

- Company **Facility- & Depotcleaning GmbH** (Kontenrahmen SKR04, 19 % USt)
- Zwei Kunden: **Nordlicht Logistik GmbH** (B2B/ZUGFeRD) und **Landesamt für Liegenschaften
  Berlin** (B2G/XRechnung mit Leitweg-ID)
- Rechnung **RE-2026-0001** → Status **Paid**, Rechnung **RE-2026-0002** → **Overdue**
- Apps installiert: `bench --site development.localhost list-apps` zeigt
  `frappe erpnext eu_einvoice erpnext_datev`

---

## Troubleshooting

- **`redis-server: not found`** → tritt bei manuellem `bench init` auf. Immer `installer.py`
  nutzen (Redis läuft in eigenen Containern).
- **`bench init` bricht mit `SyntaxError: type ... = ...` oder pip-Meldung `requires-python`** →
  Python zu alt. Frappe `version-16` braucht **Python ≥ 3.14**. Fix: `pyenv install 3.14.2`
  und Installer mit `-p 3.14.2` (Schritt 1a/1).
- **`yarn install` bricht mit `The engine "node" is incompatible ... Expected ">=24"`** →
  Node zu alt (rollt `bench init` zurück, danach `./apps.txt Not Found` bei jedem `bench`-Befehl).
  Fix: `nvm install 24 && nvm alias default 24 && npm install -g yarn`, Installer mit `-n 24`.
- **„version-16 existiert nicht"** → das ist ein **App-Branch** (in `apps.json` bzw. `-t`),
  **nicht** das `frappe_docker`-Repo. `frappe_docker` selbst bleibt auf `main`.
- **Backup-Dateien im Container nicht gefunden** → sie müssen unter
  `/workspace/development/…` liegen. Alles außerhalb von `frappe_docker/development/` ist im
  Container **nicht** sichtbar. Deshalb in Schritt 0 nach `frappe_docker/development/backup/`
  kopieren.
- **`.sql.gz` heißt `…_sql.gz` (mit Unterstrich)** → manche Upload-/Downloadwege ersetzen den
  Punkt. Vor dem Restore in `…-database.sql.gz` umbenennen (mit Punkt), sonst erkennt `restore`
  den Typ nicht.
- **Status bleibt „Unpaid" statt „Overdue"** → der Status wird von einem täglichen Job gesetzt.
  Erzwingen: `bench --site development.localhost execute frappe.utils.background_jobs.execute_job`
  ist nicht nötig – einfach kurz warten oder die Rechnung neu laden.
- **Encrypted-Fields nach Restore leer** → nur relevant bei verschlüsselten Feldern (z. B.
  E-Mail-Passwörter). Für die reine Demo ignorierbar.

---

## Versionen

Siehe `VERSIONS.md` für die exakten Versionen **und die tatsächlich installierten Commit-
Hashes** (eingetragen: frappe v16.26.3, erpnext v16.26.2). Das mitgelieferte Backup stammt
aus **Frappe 16.25.0**; frisch installiert wird die aktuelle `version-16`-Spitze, auf die
`migrate` das Backup hebt.
