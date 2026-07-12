# Schnell-Reset & vollständiger Demo-Datensatz

Ergänzung zum Haupt-Setup (siehe `README.md`). Diese Datei beschreibt **`restore_demo.sh`**
und unser **vollständiges Backup** – ohne die bestehende README zu verändern.

## Zwei Reset-Skripte / drei Backups

| Skript | Backup | Zustand |
|---|---|---|
| **`restore_demo.sh`** | `20260711_151713-…` | **Fertiger Endstand:** alles erledigt – RE-2026-0001 = **Paid** (inkl. Bank-Abgleich), RE-2026-0002 = **Overdue**, echte **Mahnung**, plus die 2 Übungs-Entwürfe. |
| **`restore_demo_live.sh`** | `20260712_112006-…` | **Live-Startpunkt:** Stand VOR den interaktiven Schritten – RE-2026-0001 **offen** (noch nicht bezahlt), **keine** Bank-Transaktionen, **keine** Mahnung (Dunning Type bleibt). Damit lassen sich Schritt 7–10 **live vorführen**. |

Das ältere Kollegen-Backup `20260710_230439-…` (ohne Bank/Mahnung) bleibt zusätzlich erhalten.

### Wann welches Skript?
- **Ergebnis zeigen / schnell zurücksetzen:** `./restore_demo.sh` → fertiger Stand.
- **Prozesse live vorführen (Bank-Import, Abgleich, Mahnung):** `./restore_demo_live.sh` → dann
  in ERPNext: Rechnung aus Timesheet (7) → XRechnung (8) → Bank-Import + Abgleich (9) → Mahnung (10).
  Danach ist der Stand ~fertig; mit `./restore_demo.sh` oder erneut `./restore_demo_live.sh` zurücksetzen.

> **Wichtig zu Schritt 9:** Der Bank-Abgleich funktioniert nur, wenn RE-2026-0001 noch **offen**
> ist. Im fertigen Stand (`restore_demo.sh`) ist sie schon *Paid* → dort findet der Abgleich
> nichts. Für die Live-Vorführung also **`restore_demo_live.sh`** nehmen.

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
