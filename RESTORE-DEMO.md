# Schnell-Reset & vollständiger Demo-Datensatz

Ergänzung zum Haupt-Setup (siehe `README.md`). Diese Datei beschreibt **`restore_demo.sh`**
und unser **vollständiges Backup** – ohne die bestehende README zu verändern.

## Zwei Reset-Skripte / drei Backups

| Skript | Backup | Zustand |
|---|---|---|
| **`restore_demo.sh`** | `20260712_140657-…` | **Fertiger Endstand:** alles erledigt – RE-2026-0001 = **Paid** (inkl. Bank-Abgleich), RE-2026-0002 = **Overdue**, echte **Mahnung**, plus die 2 Übungs-Entwürfe. |
| **`restore_demo_live.sh`** | `20260712_130230-…` | **Live-Startpunkt:** Stand VOR den interaktiven Schritten – RE-2026-0001 **offen** (noch nicht bezahlt), **keine** Bank-Transaktionen, **keine** Mahnung (Dunning Type bleibt). Damit lassen sich Schritt 7–10 **live vorführen**. |

Das ältere Kollegen-Backup `20260710_230439-…` (ohne Bank/Mahnung) bleibt zusätzlich erhalten.

> **Beide neuen Backups enthalten zwei Konto-Korrekturen**, ohne die der Bank-Abgleich (Schritt 9)
> nicht funktioniert: Standard-**Forderungskonto** = `1200` (statt 3250) und Standard-**Bankkonto**
> = `1800` (statt 1820). Sonst treffen sich Zahlung und Rechnung bzw. Zahlung und Bank-Transaktion nie.

### Wann welches Skript?
- **Ergebnis zeigen / schnell zurücksetzen:** `./restore_demo.sh` → fertiger Stand.
- **Prozesse live vorführen (Bank-Import, Abgleich, Mahnung):** `./restore_demo_live.sh` → dann
  in ERPNext: Rechnung aus Timesheet (7) → XRechnung (8) → Bank-Import + Abgleich (9) → Mahnung (10).
  Danach ist der Stand ~fertig; mit `./restore_demo.sh` oder erneut `./restore_demo_live.sh` zurücksetzen.

> **Wichtig zu Schritt 9:** Der Bank-Abgleich funktioniert nur, wenn RE-2026-0001 noch **offen**
> ist. Im fertigen Stand (`restore_demo.sh`) ist sie schon *Paid* → dort findet der Abgleich
> nichts. Für die Live-Vorführung also **`restore_demo_live.sh`** nehmen.

### Schritt 9 – so geht der Bank-Abgleich (wichtig!)
Das ERPNext-Tool kann eine **normale offene Rechnung nicht direkt** matchen (der „Ausgangsrechnung"-
Haken findet nur POS-Rechnungen). Deshalb **Zweischritt**:
1. **Import:** `docs/bank_import_neu.csv` über *Bank Statement Import* einlesen (Spalten passen 1:1,
   inkl. Pflichtspalte **Bank Account**) → 2 Bank Transactions.
2. **Bezahlen:** Rechnung `RE-2026-0001` öffnen → *Create → Payment* → **Paid To = `1800 - Bank`** →
   Submit → Rechnung **Paid**.
3. **Abgleichen:** *Bank Reconciliation Tool* → Zeile 1.332,80 € → Haken **„Zahlung" (payment_entry)**
   → den eben gebuchten Payment Entry auswählen → *Reconcile*. Zeile 250 € bleibt offen.

**Mahnung (Schritt 10):** am einfachsten direkt aus der überfälligen Rechnung `RE-2026-0002` →
*Create → Dunning* → Dunning Type „Erste Mahnung" → Submit.

### Schritt 11 – DATEV-Export (Steuerberater-Schnittstelle)
Beide Backups enthalten bereits **DATEV Settings** (Berater-Nr. `1234567`, Mandanten-Nr. `55555`,
Sachkonten-Länge 4, temp. Gegenkonto 9000). Ohne diese zeigt der DATEV-Report nichts an.
- Suche → **„DATEV"** (Report) → Company = FDC, From `01.06.2026`, To `31.07.2026`.
- Der Report listet die Buchungssätze (Soll/Haben, Konten 4400/1200/3806/1800).
- Oben rechts **„Download DATEV File"** → EXTF-CSV (Buchungsstapel) für den Steuerberater.

> Fehlen die DATEV Settings auf einer frischen Site, bietet der Report selbst einen Dialog zum
> Anlegen an. Im Echtbetrieb kommen Berater-/Mandantennummer vom Steuerberater.

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
