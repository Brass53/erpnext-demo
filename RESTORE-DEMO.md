# Schnell-Reset & vollständiger Demo-Datensatz

Ergänzung zum Haupt-Setup (siehe `README.md`). Diese Datei beschreibt **`restore_demo.sh`**
und unser **vollständiges Backup** – ohne die bestehende README zu verändern.

## Zwei Backups im `backup/`-Ordner

| Backup | Inhalt |
|---|---|
| `20260710_230439-…` | Ursprünglicher Stand: Company, Kunden, Artikel, RE-2026-0001/0002, Timesheet, Dunning **Type**. Bank-Import und Mahn-*Dokument* noch **nicht** enthalten. |
| `20260711_151713-…` **(vollständig)** | **Superset:** zusätzlich Prozess 2 (Bank-Import + Zahlungsabgleich → RE-2026-0001 = **Paid**, Payment Entry) und Prozess 3 (echte **Mahnung** `DUNN-07-26-00001`). Plus zwei **Übungs-Entwürfe** fürs Live-Vorführen. |

Beide bleiben bewusst erhalten. Wer den vollständigen Stand will, nimmt `restore_demo.sh`
(nutzt automatisch das `…151713…`-Backup).

## Die zwei Übungs-Entwürfe (fürs Live-Vorführen)

| Entwurf | Für Schritt | Inhalt |
|---|---|---|
| **TS-2026-00003** (Timesheet, Entwurf) | Schritt 6/7 | 4×8 h = 32 h, 1.120 €, Kunde A – submitten und daraus „Create Sales Invoice" zeigen |
| **RE-2026-0003** (Sales Invoice, Entwurf) | Schritt 8 | Kunde B, DL-002, 1.428 € brutto, XRECHNUNG + Leitweg-ID – submitten und „Download eInvoice" zeigen |

> Beim Vorführen entstehen daraus gebuchte Belege (die Rechnung bekommt die nächste freie
> Nummer, z. B. RE-2026-0004). Danach einfach `./restore_demo.sh` → sauberer Stand mit
> frischen Entwürfen ist wieder da.

## Nutzung

Voraussetzung: der `frappe_docker`-Dev-Container läuft (siehe README, Schritt 0–4).
Auf dem **Host** (nicht im Container):

```bash
./restore_demo.sh
```

Das Skript kopiert das vollständige Backup in den Container und spielt es per
`bench restore --with-public-files --with-private-files` ein (ohne interaktive
Passwort-Abfrage). Danach im Browser einmal hart neu laden (`Cmd/Ctrl+Shift+R`).

**Anpassbar per Umgebungsvariablen** (falls Container/Passwort abweichen):

```bash
CONTAINER=<container-name> DB_ROOT_PW=<root-pw> ./restore_demo.sh
```

- `CONTAINER` – Default `frappe_docker_devcontainer-frappe-1`
- `DB_ROOT_PW` – Default `123` (Standard-Passwort des frappe_docker-Dev-Containers)

> Hinweis: Das DB-root-Passwort ist im Dev-Container standardmäßig `123`. Es steht als
> Default im Skript, lässt sich aber wie oben per `DB_ROOT_PW` überschreiben.
