# ERPNext-Demo – Facility- & Depotcleaning GmbH

> Reproduzierbare ERPNext-Demo für das **Projekt zur Optimierung der Controllingprozesse**.
> Mit einem Befehl richtet sich jede:r im Team – und der/die Prüfende – **denselben, geprüften Stand** lokal ein: Stammdaten, E-Rechnungen (ZUGFeRD & XRechnung), automatischer Zahlungsabgleich, Mahnwesen, DATEV-Export und E-Rechnungs-Empfang.

**Team Scrumateure · Version 1.0**

---

## Inhaltsverzeichnis

- [Was ist das hier?](#was-ist-das-hier)
- [Für wen ist das gedacht?](#für-wen-ist-das-gedacht)
- [Wichtige Begriffe (kurz erklärt)](#wichtige-begriffe-kurz-erklärt)
- [Projektstruktur](#projektstruktur)
- [Voraussetzungen](#voraussetzungen)
- [Installation – Schritt für Schritt](#installation--schritt-für-schritt)
- [Demo-Daten laden](#demo-daten-laden)
- [Die drei Geschäftsprozesse (Nutzung)](#die-drei-geschäftsprozesse-nutzung)
- [Reset-Skripte & Live-Demo](#reset-skripte--live-demo)
- [Konfiguration](#konfiguration)
- [KI-Unterstützung bei der Erstellung](#ki-unterstützung-bei-der-erstellung)
- [Erklärung jeder Datei](#erklärung-jeder-datei)
- [Empfohlener Workflow](#empfohlener-workflow)
- [Fehlerbehebung](#fehlerbehebung)
- [FAQ](#faq)
- [Tipps](#tipps)
- [Entwicklerbereich](#entwicklerbereich)
- [Lizenz & Credits](#lizenz--credits)

---

## Was ist das hier?

Dieses Repository ist **nicht** ERPNext selbst. Es ist das **Rezept plus die Demo-Daten**, mit denen man eine fertig eingerichtete ERPNext-Umgebung in wenigen Minuten nachbauen kann.

ERPNext ist eine kostenlose, quelloffene **ERP-Software** (Enterprise Resource Planning – eine Software, die kaufmännische Abläufe wie Rechnungen, Buchhaltung, Personal und Lager an einem Ort abbildet). Sie läuft hier komplett **lokal in Docker-Containern** – man braucht also keinen Server und muss nichts in der Cloud betreiben.

Das Repo liefert drei Dinge:

| Baustein | Zweck |
|---|---|
| **Rezept** (`apps.json`, `VERSIONS.md`, Installations-PDF) | legt fest, welche ERPNext-Apps in welcher Version installiert werden |
| **Demo-Daten** (`backup/`) | ein komplettes Site-Backup mit fertigem, in sich stimmigem Datensatz |
| **Werkzeuge** (`scripts/`, `restore_demo*.sh`) | legen die Daten per Skript an bzw. setzen den Stand mit einem Befehl zurück |

**Welches Problem löst es?** In einem Team-/Prüfungskontext soll jede:r **exakt dieselbe** Demo sehen. Von Hand hunderte Werte einzuklicken ist fehleranfällig und nicht wiederholbar. Dieses Repo macht den Stand **reproduzierbar**: einmal Backup einspielen – fertig.

**Wie funktioniert es grundsätzlich?**

```text
frappe_docker (offizielles Docker-Rezept)   +   dieses Repo (Apps + Daten)
                         │
                         ▼
        ERPNext läuft lokal im Container
                         │
                         ▼
      Demo-Backup einspielen  →  fertiger Stand
```

---

## Für wen ist das gedacht?

- **Teammitglieder**, die lokal denselben Stand brauchen wie alle anderen.
- **Prüfende/Dozierende**, die die Demo mit einem Befehl starten wollen.
- **Alle ohne ERPNext-Vorwissen** – die Installations-PDF und diese README führen Schritt für Schritt durch alles.

---

## Wichtige Begriffe (kurz erklärt)

| Begriff | Bedeutung in einfachen Worten |
|---|---|
| **ERPNext** | Die kaufmännische Software (Rechnungen, Buchhaltung, …). |
| **Frappe / Bench** | Das technische Fundament unter ERPNext. `bench` ist das Kommandozeilen-Werkzeug dazu. |
| **Docker / Container** | Eine „Kiste", in der die Software isoliert läuft – nichts wird direkt auf dem Rechner installiert. |
| **Dev Container** | Ein von VS Code gestarteter Container, in dem entwickelt wird. |
| **Site** | Eine ERPNext-Instanz mit eigener Datenbank – bei uns `development.localhost`. |
| **DocType** | Ein Datensatz-Typ in ERPNext (z. B. „Kunde", „Ausgangsrechnung"). |
| **SKR04** | Ein deutscher Standard-Kontenrahmen (die Nummerierung der Buchungskonten). |
| **ZUGFeRD / XRechnung** | Zwei Formate für **elektronische Rechnungen**. XRechnung (reines XML) ist bei Behörden Pflicht, ZUGFeRD (PDF mit eingebettetem XML) üblich im B2B. |
| **DATEV** | Software des Steuerberaters; ERPNext exportiert die Buchungen in ein DATEV-Format. |

---

## Projektstruktur

```text
erpnext-demo/
│
├── README.md                     ← diese Datei
├── apps.json                     ← Liste der ERPNext-Apps (das „Rezept")
├── VERSIONS.md                   ← exakte Versionen/Commit-Hashes, die bei uns laufen
├── RESTORE-DEMO.md               ← Doku zu den Reset-Skripten (Details zur Demo)
│
├── restore_demo.sh               ← Reset auf den FERTIGEN Endstand (ein Befehl)
├── restore_demo_live.sh          ← Reset auf den LIVE-Demo-Startpunkt (ein Befehl)
│
├── scripts/
│   └── seed_demo.py              ← legt die Demo-Daten per Skript an (Alternative zum Backup)
│
├── backup/                       ← Demo-Site-Backups (DB + Dateien) — bewusst eingecheckt
│   ├── 20260712_144126-…         ← fertiger Endstand
│   ├── 20260717_083148-…         ← Live-Demo-Startpunkt
│   └── 20260710_230439-…         ← älterer Stand (Referenz)
│
└── docs/
    ├── ERPNext-lokal-installieren.pdf     ← Installations-Anleitung (Hauptquelle Setup)
    ├── ERPNext-KI-Unterstuetzung.pdf      ← wie KI beim Aufbau geholfen hat
    ├── Testdaten-Spezifikation.pdf        ← WAS die Demo an Daten braucht (Vorgabe)
    ├── Testdaten-und-Einpflege-Anleitung.md  ← konkreter Datensatz + Klick-Anleitung
    ├── bank_import.csv                     ← Bank-CSV (Original)
    └── bank_import_neu.csv                 ← Bank-CSV (ERPNext-gerechte Spalten)
```

> [!NOTE]
> Der Ordner `backup/` wird **absichtlich mit eingecheckt** (nur ~1 MB pro Datenbank), damit der Demo-Stand ohne Umwege wiederherstellbar ist. Die eigentliche ERPNext-Software (Bench, `node_modules` usw.) gehört **nicht** ins Repo – sie wird bei der Installation frisch geladen. Details siehe [`.gitignore`](.gitignore).

---

## Voraussetzungen

Auf dem Rechner installiert sein müssen (mehr nicht – Python, Node, Datenbank usw. laufen alle im Container):

| Werkzeug | Wofür |
|---|---|
| **Docker Desktop** | führt die Container aus (mind. ~8 GB RAM frei) |
| **Visual Studio Code** | Editor, startet den Dev Container |
| **VS-Code-Extension „Dev Containers"** | verbindet VS Code mit dem Container |
| **Git** | lädt die Repos herunter |

Kurz prüfen, ob alles da ist (im Terminal):

```bash
docker --version
docker compose version
git --version
```

> [!TIP]
> **Apple Silicon (M-Chips):** In Docker Desktop unter *Settings → General* die Option **„Rosetta"** aktivieren – sonst kann der Build fehlschlagen.

---

## Installation – Schritt für Schritt

> Hauptquelle: [`docs/ERPNext-lokal-installieren.pdf`](docs/ERPNext-lokal-installieren.pdf). Unten ist jeder Schritt zusätzlich erklärt: **warum** man ihn macht, **was** dabei passiert und **was tun**, wenn ein Fehler kommt.

### 1. ERPNext-Docker-Rezept herunterladen

```bash
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker
```

**Warum:** `frappe_docker` ist das offizielle Rezept, das die Container-Umgebung für ERPNext bereitstellt.
**Was passiert:** Es entsteht ein Ordner `frappe_docker` mit allen Container-Vorlagen.

### 2. Projekt im Dev Container öffnen

```bash
code .
```

Dann in VS Code: **`Cmd + Shift + P`** (Mac) bzw. **`Strg + Shift + P`** (Windows) → **„Dev Containers: Reopen in Container"** wählen und warten, bis der Container vollständig gestartet ist.

**Warum:** So läuft alles isoliert im Container – auf dem Rechner selbst wird nichts installiert.
**Was passiert:** VS Code baut den Container (beim ersten Mal einige Minuten) und öffnet ein Terminal **im** Container. Der Prompt sieht dann etwa so aus: `frappe@…:/workspace/development$`.

> [!IMPORTANT]
> **Ab hier laufen alle `bench`-Befehle im Container-Terminal**, nicht im normalen Mac/Windows-Terminal. Nur `docker`, `git` und die Reset-Skripte (`restore_demo*.sh`) laufen außerhalb, auf dem Host.

### 3. In den Development-Ordner wechseln

```bash
cd development
```

**Warum:** Alles unter `frappe_docker/development/` ist im Container als `/workspace/development/` sichtbar – hier wird die Bench angelegt.

### 4. ERPNext installieren

```bash
python installer.py
```

Während der Installation werden Angaben abgefragt. Beispielwerte:

| Frage | Beispielwert |
|---|---|
| ERPNext Version | `version-16` |
| Site Name | `development.localhost` |
| Administrator Password | `admin` |
| MariaDB Root Password | `admin` |

**Warum:** Der Installer richtet Bench, Datenbank, ERPNext und die Website automatisch ein.
**Was passiert:** Es entsteht der Ordner `frappe-bench/` mit der neuen Site `development.localhost`.

> [!WARNING]
> **Häufigster Fehler beim ersten Build:** Bricht `installer.py` mit `SyntaxError: type ... = ...` (Python) oder `The engine "node" is incompatible … Expected ">=24"` (Node/yarn) ab, ist die Laufzeit im Container zu alt. Die aktuelle `version-16` verlangt **Python ≥ 3.14** und **Node ≥ 24**. Behebung siehe [Fehlerbehebung](#1-installer-bricht-ab-python--node-zu-alt).

### 5. In die Bench wechseln

```bash
cd frappe-bench
```

### 6. ERPNext starten

```bash
bench start
```

ERPNext ist danach erreichbar unter **http://development.localhost:8000** (Login: `Administrator` / das oben gesetzte Passwort).

**Was passiert:** `bench start` startet den Webserver und die Hintergrundprozesse. Das Terminal bleibt belegt – **offen lassen**, solange ERPNext laufen soll.

### 7. Setup-Assistent durchführen

Beim ersten Login:

- **Company** anlegen: `Facility- & Depotcleaning GmbH`
- **Land:** Deutschland · **Währung:** EUR
- **Kontenrahmen:** **SKR04 (mit Kontonummern)**
- Administrator einrichten

**Warum:** Ohne Company und Kontenrahmen kann ERPNext keine Belege buchen.

> [!TIP]
> Wer direkt den fertigen Demo-Stand will, kann den Setup-Assistenten knapp durchklicken und danach einfach das **Demo-Backup** einspielen (siehe [Demo-Daten laden](#demo-daten-laden)) – das überschreibt den Stand ohnehin.

### 8. Backup erstellen (vor weiteren Apps)

```bash
bench --site development.localhost backup
```

**Warum:** Ein Sicherungspunkt, bevor zusätzliche Apps installiert werden.

### 9. X-Rechnung installieren (App `eu_einvoice`)

```bash
bench get-app https://github.com/alyf-de/eu_einvoice.git
bench --site development.localhost install-app eu_einvoice
bench --site development.localhost migrate
```

**Warum:** `eu_einvoice` liefert die E-Rechnungs-Felder und den ZUGFeRD/XRechnung-Export **und** den Empfang von E-Rechnungen.
**Was passiert:** `get-app` lädt den Code, `install-app` aktiviert ihn auf der Site, `migrate` bringt die Datenbank auf den passenden Stand.

### 10. DATEV-App installieren (App `erpnext_datev`)

```bash
bench get-app https://github.com/alyf-de/erpnext_datev.git
bench --site development.localhost install-app erpnext_datev
bench --site development.localhost migrate
```

**Warum:** `erpnext_datev` erzeugt den DATEV-Export für den Steuerberater.

### 11. Cache leeren

```bash
bench clear-cache
bench clear-website-cache
```

**Warum:** Nach App-Installationen kann die Oberfläche veraltete Menüs zeigen – Cache leeren + Browser neu laden behebt das.

### 12. Installierte Apps prüfen

```bash
bench --site development.localhost list-apps
```

Erwartete Ausgabe (Reihenfolge kann abweichen):

```text
frappe
erpnext
payments
hrms
eu_einvoice
erpnext_datev
```

**Fertig** – ERPNext läuft lokal unter **http://development.localhost:8000** mit ERPNext, HRMS, X-Rechnung und DATEV-Export.

### Wichtige Bench-Befehle (Nachschlagen)

| Aufgabe | Befehl |
|---|---|
| ERPNext starten | `bench start` |
| Migration durchführen | `bench --site development.localhost migrate` |
| Backup erstellen | `bench --site development.localhost backup` |
| Cache leeren | `bench clear-cache` / `bench clear-website-cache` |
| Installierte Apps anzeigen | `bench --site development.localhost list-apps` |
| Versionen anzeigen | `bench version` |

---

## Demo-Daten laden

Es gibt **zwei Wege**, an den fertigen Datensatz zu kommen. Für die Präsentation ist Weg A am einfachsten.

### Weg A – Backup einspielen (empfohlen)

Das mitgelieferte Backup enthält den kompletten, geprüften Datensatz (2 Kunden, 2 Artikel, Rechnungen, Zahlung, Mahnung, DATEV-Einstellungen). Im Container ausführen:

```bash
BK=/workspace/development/erpnext-demo/backup
bench --site development.localhost restore \
  $BK/20260712_144126-development_localhost-database.sql.gz \
  --with-public-files  $BK/20260712_144126-development_localhost-files.tar \
  --with-private-files $BK/20260712_144126-development_localhost-private-files.tar
bench --site development.localhost migrate
```

> [!NOTE]
> Damit das Backup im Container sichtbar ist, muss dieses Repo unter `frappe_docker/development/erpnext-demo` liegen (oder der `backup/`-Ordner dorthin kopiert werden). Noch bequemer geht das mit den **Reset-Skripten** (siehe unten) – die erledigen das Kopieren automatisch.

`restore` **überschreibt** die Site mit dem Demo-Stand. Weicht das Admin-Passwort ab, zurücksetzen mit:

```bash
bench --site development.localhost set-admin-password admin
```

### Weg B – Daten per Skript neu anlegen

Wer die Werte lieber frisch eintragen lassen will (z. B. um etwas zu ändern), nutzt [`scripts/seed_demo.py`](scripts/seed_demo.py). Das Skript ist **idempotent** – mehrfaches Ausführen erzeugt keine Duplikate. Im Container:

```bash
echo "exec(open('/workspace/development/erpnext-demo/scripts/seed_demo.py').read(), globals())" \
  | bench --site development.localhost console
```

Es legt an: Company-Stammdaten, Steuervorlage 19 %, Bank + Bankkonto, Zahlungsbedingungen, beide Kunden, beide Artikel, Mitarbeiter + Zeiterfassung, beide Rechnungen, die Zahlung und den Mahn-Typ. Am Ende erscheint eine Zusammenfassung.

---

## Die drei Geschäftsprozesse (Nutzung)

Die Demo bildet den Controlling-Ablauf in **drei Prozessen** ab. Die fachliche Klick-Anleitung mit allen Werten steht in [`docs/Testdaten-und-Einpflege-Anleitung.md`](docs/Testdaten-und-Einpflege-Anleitung.md).

### Prozess 1 – Rechnung & E-Rechnung

Aus einer Zeiterfassung (Timesheet) entsteht **Rechnung A** an Kunde A (Nordlicht Logistik GmbH) als **ZUGFeRD**. **Rechnung B** an die Behörde (Landesamt) wird als **XRechnung** erstellt. Beide E-Rechnungen lassen sich über das eu_einvoice-Menü herunterladen.

> [!IMPORTANT]
> **Die Datenkette (nicht verändern):** 35,00 € × 32 h = **1.120,00 € netto** → + 19 % USt = **1.332,80 € brutto** (Rechnung A). Genau dieser Betrag steht später auf dem Kontoauszug, und die Rechnungsnummer **RE-2026-0001** steht im Verwendungszweck. Ändert man einen Wert, muss die ganze Kette angepasst werden.

### Prozess 2 – Zahlungseingang & automatischer Abgleich

Ein Kontoauszug (CSV) wird importiert. Trägt die Bank-Buchung die **Rechnungsnummer im Verwendungszweck**, ordnet ERPNext sie **automatisch** der richtigen Rechnung zu. Eine zweite Zahlung ohne Referenz bleibt bewusst offen – das zeigt, dass wirklich über den Verwendungszweck zugeordnet wird und nicht über den Betrag.

Ablauf: **Kontoauszug importieren → Zahlung erfassen (mit Referenznummer) → „Automatisch abgleichen"**. Ergebnis: Rechnung A = **Bezahlt**, die 250-€-Zeile bleibt offen.

### Prozess 3 – Mahnwesen

Rechnung B ist überfällig. Direkt aus der überfälligen Rechnung → **Erstellen → Mahnung** → Mahnart „Erste Mahnung" (5,00 € Gebühr, 9,12 % Zinsen) → buchen → als PDF drucken.

### Ergänzend: DATEV-Export & E-Rechnungs-Empfang

- **DATEV:** Bericht „DATEV" öffnen, Unternehmen + Zeitraum wählen → **DATEV-Datei herunterladen** (die Datei für den Steuerberater).
- **E-Rechnung empfangen:** Eine erhaltene XRechnung über **E-Rechnungs-Import** einlesen; ERPNext prüft sie automatisch und erzeugt daraus eine **Eingangsrechnung**.

---

## Reset-Skripte & Live-Demo

Damit man vor jeder Vorführung sauber zurücksetzen kann, gibt es zwei Ein-Befehl-Skripte. Sie laufen auf dem **Host** (nicht im Container) und spielen das passende Backup ein. Details: [`RESTORE-DEMO.md`](RESTORE-DEMO.md).

| Skript | Zustand danach | Wofür |
|---|---|---|
| **`./restore_demo.sh`** | fertiger Endstand (alles erledigt) | Ergebnis zeigen / schneller Reset / Notfall-Fallback |
| **`./restore_demo_live.sh`** | Live-Demo-Startpunkt (Ein-Klick-Auto-Reconcile vorbereitet) | Prozesse live vorführen |

```bash
cd erpnext-demo
./restore_demo.sh        # oder: ./restore_demo_live.sh
```

Danach im Browser einmal hart neu laden (`Cmd/Ctrl + Shift + R`).

> [!TIP]
> Container-Name und Datenbank-Passwort sind überschreibbar, falls sie bei dir abweichen:
> ```bash
> CONTAINER=<container-name> DB_ROOT_PW=<root-pw> ./restore_demo.sh
> ```
> Standard: Container `frappe_docker_devcontainer-frappe-1`, Passwort `123` (Standard des Dev-Containers).

---

## Konfiguration

### `apps.json` – welche Apps in welcher Version

```json
[
  { "url": "https://github.com/frappe/erpnext",        "branch": "version-16" },
  { "url": "https://github.com/alyf-de/eu_einvoice",   "branch": "develop" },
  { "url": "https://github.com/alyf-de/erpnext_datev", "branch": "version-16" }
]
```

Das ist das maschinenlesbare Gegenstück zur Installations-PDF. Wichtig: hier stehen **Branches**, keine festen Commits – ein späterer Build kann also einen neueren Stand ziehen. Wer **exakt** unseren Stand will, nimmt die Commit-Hashes aus [`VERSIONS.md`](VERSIONS.md).

### Wichtige Einstellungen im Datensatz

Diese Werte sind im Backup schon korrekt gesetzt. Beim manuellen Aufbau unbedingt beachten:

| Einstellung | Wert | Warum wichtig |
|---|---|---|
| Standard-Forderungskonto | **1200** | sonst finden Zahlung und Rechnung nie zusammen (Bank-Abgleich scheitert) |
| Standard-Bankkonto | **1800** | die importierten Bank-Buchungen liegen auf 1800 – Zahlung muss dorthin |
| DATEV-Einstellungen | Berater-/Mandantennr. gesetzt | ohne sie zeigt der DATEV-Bericht **nichts** an |
| Verkäufer-Kontakt | E-Mail **und** Telefon | Pflicht (BT-34/BT-42), sonst ist die XRechnung ungültig |
| Käufer-Kontakt | E-Mail | Pflicht (BT-49), sonst ist die XRechnung ungültig |

### Standardwerte / Zugänge

| Was | Wert |
|---|---|
| URL | http://development.localhost:8000 |
| Login | `Administrator` / `admin` |
| Site | `development.localhost` |
| Container | `frappe_docker_devcontainer-frappe-1` |
| Kontenrahmen | SKR04 · Geschäftsjahr 2026 |

---

## KI-Unterstützung bei der Erstellung

> Quelle: [`docs/ERPNext-KI-Unterstuetzung.pdf`](docs/ERPNext-KI-Unterstuetzung.pdf).

Beim Aufbau der Demo hat uns eine KI (Claude Opus 4.8) geholfen – **nicht** als Bestandteil der laufenden Software, sondern als Werkzeug bei Einrichtung, Prüfung und Dokumentation. Die KI hatte dabei ausschließlich Zugriff auf den Projektordner und den Docker-Container.

**Wobei die KI konkret geholfen hat:**

- **Ist-Analyse:** über die Bench-Console prüfen, was schon existiert und was fehlt.
- **Anlegen:** Konfiguration und Testdaten **per Skript** statt hunderter Klicks.
- **Prüfen:** Abgleich gegen die Konsistenz-Checkliste der Spezifikation.
- **Fehler finden:** z. B. zwei falsch gesetzte Standardkonten (Bank-Abgleich unmöglich) und eine ungültige XRechnung (fehlende Käufer-E-Mail / Verkäufer-Telefon).
- **Reproduzierbarkeit:** Backups und Reset-Skripte.
- **Repo & Hilfsdateien:** Aufbau des Repos und der Helfer-Skripte (`.py`, `.sh`), damit ERPNext wirklich lauffähig wurde.
- **Doku:** Anleitungen und Befehlsübersichten prüfen und anpassen.

### Zugriff geben

Die KI kann nur mit Ordnern arbeiten, die ihr freigegeben sind. Deshalb die zu verarbeitenden Dateien einmal in den Projektordner kopieren:

```bash
cp ~/Downloads/testdaten.pdf ~/projektordner/
```

> [!NOTE]
> **macOS-Besonderheit:** Der Ordner `~/Downloads` ist vom System besonders geschützt – dort bekommt die KI selbst mit Freigabe keinen Zugriff („Operation not permitted"). Deshalb Dateien immer erst in den **Projektordner** kopieren.

### Beispiel-Prompts (zum Nachmachen)

So kann jemand dasselbe reproduzieren. Wichtig ist die Reihenfolge: **erst analysieren, dann anlegen, dann prüfen** – nicht alles in einem Rutsch.

**1) Analysieren – erst schauen, nichts ändern**
> „Im Projektordner liegt `testdaten.pdf`. ERPNext läuft im Container `frappe_docker_devcontainer-frappe-1`, Site `development.localhost`. Lies die Spezifikation, prüfe per Bench-Console den Ist-Zustand und zeig mir eine Soll/Ist-Gegenüberstellung. **Lege noch nichts an.**"

*Sinn:* Man versteht zuerst, was schon da ist und was fehlt – ohne etwas kaputt zu machen. Prompt so lange anpassen, bis die Analyse stimmt.

**2) Einrichten & anlegen – schrittweise und wiederholbar**
> „Lege die fehlende Konfiguration und die Testdaten per Skript in der Bench-Console an. Das Skript muss **wiederholbar** sein und bei erneuter Ausführung **keine Duplikate** erzeugen. Reihenfolge: zuerst Stammdaten (Company, Bank, Zahlungsbedingungen, Kunden, Artikel), anschließend Belege (Zeiterfassung, Rechnungen, Zahlung, Mahnung). **Verifiziere nach jeder Stufe.**"

*Sinn:* Ein wiederholbares Skript kann man gefahrlos erneut laufen lassen. Die feste Reihenfolge verhindert Abhängigkeitsfehler (Rechnungen brauchen Kunden und Artikel).

**3) Prüfen & sichern**
> „Prüfe den Datensatz gegen die Checkliste und erstelle ein Backup samt Skript, mit dem wir den Stand jederzeit wiederherstellen können."

*Sinn:* Am Ende steht ein geprüfter, jederzeit wiederherstellbarer Stand.

### Learnings (ehrlich)

- **Erst analysieren, dann anlegen** – und nach jeder Stufe kontrollieren.
- **Angaben zur Oberfläche verifizieren:** Bei Menüpunkten lag die KI teils daneben, bis sie im Quellcode nachsah. Ergebnisse immer im System gegenprüfen.
- **Die Stärke der KI lag im Prüfen, nicht im Klicken:** Sie fand Fehler, die beim manuellen Einpflegen unentdeckt geblieben wären.

---

## Erklärung jeder Datei

Für Einsteiger: was jede Datei ist und wann man sie anfasst.

### `README.md`
Diese Datei – der zentrale Einstieg ins Projekt.
**Bearbeiten?** Nur wenn sich am Projekt etwas ändert.

### `apps.json`
Die Liste der ERPNext-Apps mit Repository-URL und Branch (siehe [Konfiguration](#konfiguration)). Das „Rezept", welche Apps installiert werden.
**Bearbeiten?** Nur wenn eine App dazukommt/wegfällt oder ein anderer Branch gewünscht ist.

### `VERSIONS.md`
Hält die **exakten Versionen und Commit-Hashes** fest, mit denen die Demo läuft. Für die exakte Reproduktion.
**Bearbeiten?** Wenn ein neues Backup mit anderen Versionen erstellt wurde.

### `RESTORE-DEMO.md`
Ausführliche Doku zu den beiden Reset-Skripten und zum Live-Demo-Ablauf (welches Skript wofür, Ein-Klick-Auto-Reconcile, Konto-Korrekturen).
**Bearbeiten?** Wenn sich der Demo-Ablauf ändert.

### `restore_demo.sh`
Shell-Skript (läuft auf dem **Host**). Spielt in einem Befehl das Backup des **fertigen Endstands** ein.
**Bearbeiten?** Nur wenn Container-Name, Passwort oder Backup-Datei wechseln – dafür gibt es aber die Umgebungsvariablen `CONTAINER` und `DB_ROOT_PW`.

### `restore_demo_live.sh`
Wie oben, aber setzt auf den **Live-Demo-Startpunkt** zurück (Kontoauszug + Zahlung liegen vorbereitet, damit man nur „Automatisch abgleichen" klicken muss).

### `scripts/seed_demo.py`
Python-Skript, das den **gesamten Demo-Datensatz per Bench-Console anlegt** – idempotent (mehrfach ausführbar ohne Duplikate). Die Alternative zum Backup, wenn man die Daten frisch eintragen will.
**Bearbeiten?** Wenn sich Werte des Datensatzes ändern sollen.

### `backup/…`
Die Demo-Site-Backups: je Stand drei Dateien – Datenbank (`…-database.sql.gz`), öffentliche Dateien (`…-files.tar`) und private Dateien (`…-private-files.tar`).
**Bearbeiten?** Nie von Hand – nur über `bench backup` neu erzeugen.

### `docs/ERPNext-lokal-installieren.pdf`
Die **Installations-Anleitung** des Teams (Hauptquelle für das Setup oben).
**Bearbeiten?** Beim Aktualisieren der Installationsschritte.

### `docs/ERPNext-KI-Unterstuetzung.pdf`
Beschreibt, **wie die KI beim Aufbau geholfen hat**, inklusive Beispiel-Prompts und Learnings (siehe [KI-Unterstützung](#ki-unterstützung-bei-der-erstellung)).

### `docs/Testdaten-Spezifikation.pdf`
Die **Vorgabe**: welche Daten und Beziehungen die Demo braucht (mit 🔒-Ankern, die exakt zusammenpassen müssen, und ✏️-Feldern, die frei ausgeschmückt werden dürfen). Enthält die **Konsistenz-Checkliste**.

### `docs/Testdaten-und-Einpflege-Anleitung.md`
Setzt die Spezifikation in **konkrete Werte** um und liefert die **Klick-Anleitung** (Teil A = Datensatz, Teil B = Schritt-für-Schritt). Das inhaltliche Kern-Dokument.

### `docs/bank_import.csv`
Die Bank-CSV für Prozess 2, wie in der Spezifikation beschrieben (Spalten: Datum, Betrag, Verwendungszweck, Auftraggeber).

### `docs/bank_import_neu.csv`
Dieselben Buchungen, aber mit **ERPNext-gerechten Spaltennamen** (Date, Deposit, Description, Reference Number, **Bank Account**), damit der Import ohne manuelles Zuordnen durchläuft. Die Spalte **Bank Account** ist Pflicht.
**Verwenden?** Für den Bank-Import in Prozess 2 – der bequemere der beiden.

### `.gitignore`
Legt fest, was **nicht** ins Repo gehört (die Bench, `node_modules`, Caches …) und dass das Demo-Backup bewusst **doch** eingecheckt wird.

---

## Empfohlener Workflow

```text
Installation (frappe_docker + Dev Container + installer.py)
        ↓
Apps installieren (eu_einvoice, erpnext_datev)
        ↓
Demo-Daten laden (Backup einspielen  ODER  seed_demo.py)
        ↓
Prozesse ansehen/vorführen (Rechnung → Zahlung → Mahnung → DATEV → E-Rechnung)
        ↓
Vor jeder Vorführung: ./restore_demo_live.sh   (sauberer Startpunkt)
        ↓
Bei Bedarf erweitern / eigene Daten importieren (Data Import)
```

---

## Fehlerbehebung

### 1. Installer bricht ab (Python / Node zu alt)
**Problem:** `bench init` / `installer.py` stoppt mit `SyntaxError: type … = …` oder `The engine "node" is incompatible … Expected ">=24"`.
**Ursache:** Die aktuelle `version-16` verlangt **Python ≥ 3.14** und **Node ≥ 24**; das Standard-Image bringt oft ältere Versionen mit.
**Lösung:** Im Container die passenden Versionen bereitstellen und den Installer mit den Flags starten:
```bash
pyenv install -s 3.14.2
nvm install 24 && nvm alias default 24 && npm install -g yarn
python installer.py -j apps.json -s development.localhost \
  -r https://github.com/frappe/frappe -t version-16 -p 3.14.2 -n 24 -v
```

### 2. `redis-server: not found`
**Ursache:** Tritt bei manuellem `bench init` auf. **Lösung:** Immer `installer.py` nutzen – Redis läuft in eigenen Containern.

### 3. DATEV-Bericht zeigt nichts an
**Ursache:** Es fehlen der Zeitraum-Filter **oder** die DATEV-Einstellungen.
**Lösung:** Unternehmen **und** Von-/Bis-Datum setzen (beide im **selben Geschäftsjahr**). Fehlen die DATEV-Einstellungen (Berater-/Mandantennr.), bietet der Bericht einen Dialog zum Anlegen an.

### 4. Bank-Abgleich findet die Rechnung nicht / Zahlung nicht zuordenbar
**Ursache:** Meist stimmen die Konten nicht (Standard-Forderungskonto ≠ Rechnungskonto, Standard-Bankkonto ≠ Kontoauszug-Konto), oder die Referenznummer fehlt an der Zahlung.
**Lösung:** Standard-Forderungskonto **1200** und Standard-Bankkonto **1800** setzen; die Zahlung mit der **Rechnungsnummer als Referenz** erfassen und auf Konto 1800 buchen. (Im Demo-Backup ist das bereits korrekt.)

### 5. XRechnung ist „rot" / ungültig
**Ursache:** Ein Pflichtfeld fehlt.
**Lösung:** Prüfen, dass vorhanden sind: Verkäufer-**USt-IdNr.**, **IBAN**, Verkäufer-**E-Mail** und **Telefon**, Käufer-**E-Mail** (BT-49), **Leistungszeitraum** (BT-72) und bei Behörden die **Leitweg-ID**.

### 6. Rechnung wird nicht „Overdue"
**Ursache:** Der Status wird von einem täglichen Hintergrundjob gesetzt.
**Lösung:** Kurz warten oder die Rechnung neu laden – für die Demo reicht meist „Unpaid + Fälligkeit rot".

### 7. Rechnungsnummer wird `ACC-SINV-…` statt `RE-2026-…`
**Ursache:** Ohne eigene Nummernserie vergibt ERPNext den Standard.
**Lösung:** Vorher die Serie `RE-2026-` anlegen **oder** die tatsächliche Nummer im Verwendungszweck der Bank-CSV nachziehen.

### 8. Datei-Import: „Sales Invoice" wird nicht gefunden
**Ursache:** Die Oberfläche ist deutsch. **Lösung:** „**Ausgangsrechnung**" tippen (Dokumententyp wird **ausgewählt**, nicht erstellt). Für Eingangsrechnungen: „Eingangsrechnung".

---

## FAQ

**Muss ich programmieren können?**
Nein. Für Installation und Demo genügt es, die Befehle aus dieser README zu kopieren.

**Brauche ich eine Internetverbindung?**
Für die Installation ja (Apps werden heruntergeladen). Danach läuft die Demo lokal.

**Wird der Rechner „zugemüllt"?**
Nein. Alles läuft in Docker-Containern; ERPNext selbst wird nicht direkt installiert.

**Backup oder Skript – was nehmen?**
Backup (Weg A) für den schnellsten, garantiert identischen Stand. Skript (`seed_demo.py`) nur, wenn man die Daten frisch/anders anlegen will.

**Kann ich eigene Daten importieren?**
Ja – über **Datenimport** (z. B. Ausgangsrechnungen aus Excel). Kunden und Artikel müssen vorher existieren.

**Nutzt die laufende Software KI?**
Nein. KI wurde nur beim **Aufbau** verwendet (siehe [KI-Unterstützung](#ki-unterstützung-bei-der-erstellung)), nicht im Betrieb.

---

## Tipps

- **Backups:** Vor größeren Änderungen `bench --site development.localhost backup` – oder einfach eines der Reset-Skripte nutzen.
- **Wartung/Updates:** Nach dem Ziehen neuer App-Versionen immer `bench … migrate` und danach `bench clear-cache`.
- **Performance:** Docker Desktop genügend RAM geben (≈ 8 GB). Das belegte `bench start`-Terminal offen lassen.
- **Sicherheit:** Die Passwörter (`admin`, `123`) sind reine **Demo-Werte**. Für echten Betrieb ersetzen und die Test-USt-IdNr./IBAN durch echte Daten austauschen.
- **Reproduzierbarkeit:** Für exakt denselben Stand die Commit-Hashes aus [`VERSIONS.md`](VERSIONS.md) fixieren – `apps.json` pinnt nur Branches.

---

## Entwicklerbereich

**Architektur (grob):**

```text
Host (Mac/Windows)
 └─ Docker Desktop
     └─ Dev-Container "frappe_docker_devcontainer-frappe-1"
         └─ Frappe Bench  (/workspace/development/frappe-bench)
             ├─ App: frappe        (Fundament)
             ├─ App: erpnext       (+ hrms, payments)
             ├─ App: eu_einvoice   (ZUGFeRD / XRechnung, E-Rechnungs-Empfang)
             └─ App: erpnext_datev (DATEV-Export)
             └─ Site: development.localhost  (MariaDB-Datenbank)
```

**„Build"-Prozess:** Es gibt keinen klassischen Build. Der Aufbau ist: `frappe_docker` klonen → Dev Container → `installer.py` → Apps via `bench get-app` → Daten via Backup/`seed_demo.py`.

**Abhängigkeiten:** Definiert durch `apps.json` (Apps) und `VERSIONS.md` (exakte Commits). Laufzeit: Python ≥ 3.14, Node ≥ 24, MariaDB, Redis – alles im Container.

**Erweitern:** Weitere Apps mit `bench get-app <url>` + `bench --site … install-app <app>` + `migrate`. Eigene Massendaten über **Datenimport** (Excel/CSV).

**Datenmodell (Kern-DocTypes der Demo):** Company, Customer, Item, Employee, Timesheet, Sales Invoice, Payment Entry, Bank Transaction, Dunning – die Beziehungen sind in [`docs/Testdaten-Spezifikation.pdf`](docs/Testdaten-Spezifikation.pdf) beschrieben.

---

## Lizenz & Credits

- **Projekt:** Optimierung der Controllingprozesse · Kunde *Facility- & Depotcleaning GmbH* · **Team Scrumateure**.
- **Verwendete Open-Source-Software:** [ERPNext](https://github.com/frappe/erpnext) & [Frappe](https://github.com/frappe/frappe) (GNU GPL v3), [eu_einvoice](https://github.com/alyf-de/eu_einvoice) und [erpnext_datev](https://github.com/alyf-de/erpnext_datev) (ALYF GmbH).
- Teile der Einrichtung, Prüfung und Dokumentation entstanden mit **KI-Unterstützung** (Claude) und wurden vom Team auf Richtigkeit geprüft.
