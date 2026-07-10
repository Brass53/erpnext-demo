# VERSIONS – exakter Stand unserer Demo

Diese Datei hält fest, mit welchen Versionen die Demo läuft. Wer 1:1 unseren Zustand
reproduzieren will, nutzt diese Angaben. Das mitgelieferte Backup (`20260710_224015-…`)
wurde mit **Frappe 16.26.3** erzeugt und enthält den **vollständigen Demo-Datensatz**
(2 Kunden, 2 Artikel, Rechnungen RE-2026-0001/0002, Zahlung, Timesheet, Mahn-Typ). Frisch
installiert wird die jeweils aktuelle `version-16`-Spitze, auf die `migrate` das Schema hebt.

> ⚠️ **Wichtige Korrektur (2026-07-10):** Die früher hier genannten Werte
> „Python 3.11.9" / nur `frappe/bench:v5.27.0" reichen **nicht**. Die aktuelle
> `version-16` verlangt **Python ≥ 3.14** *und* **Node ≥ 24** (sogar der Tag
> `v16.25.0` hat `requires-python = ">=3.14"`). Mit Python 3.11 / Node 20 bricht
> `bench init` ab. Siehe README, Schritt 1.

## Framework / Bench

| Komponente | Version / Branch | Quelle |
|---|---|---|
| Frappe Framework (installiert) | **16.26.3** (branch `version-16`) | `bench version` |
| Frappe Framework (Backup, vollständig) | **16.26.3** | neues Backup `20260710_224015-…-database.sql.gz` |
| MariaDB (Server, im Container) | 11.8.x | `.devcontainer/docker-compose.yml` |
| **Python (Installer-Flag)** | **3.14.2** | `-p 3.14.2` in `installer.py` (via `pyenv install 3.14.2` im Container) |
| **Node (Installer-Flag)** | **24** | `-n 24` in `installer.py` (via `nvm install 24` im Container) |
| Bench-Image (gepinnt) | **frappe/bench:v5.27.0** | `.devcontainer/docker-compose.yml`, Zeile 44 – bringt nur Python 3.11 / Node 20 mit, daher werden 3.14 + Node 24 im Container nachinstalliert |

## Apps (aus `apps.json`)

| App | Branch | Repo |
|---|---|---|
| erpnext | `version-16` | https://github.com/frappe/erpnext |
| eu_einvoice | `develop` | https://github.com/alyf-de/eu_einvoice |
| erpnext_datev | `version-16` | https://github.com/alyf-de/erpnext_datev |

## Tatsächlich installierte Commits (Stand 2026-07-10)

| App | Version | Commit-Hash |
|---|---|---|
| frappe | v16.26.3 | `4113465d23888d70936bb332fd9110ab4330cbf1` |
| erpnext | v16.26.2 | `d1d3b241ae7bc21d18cf830a4bacd568e21a2a19` |
| eu_einvoice | develop | `e67191ca0038762f2c11ba945c8df3300ec4913c` |
| erpnext_datev | version-16 | `8c4c25f19ed90b88c87d0a7f2b69ff348b04b644` |

Neu ermitteln (im Container):

```bash
cd /workspace/development/frappe-bench
for app in frappe erpnext eu_einvoice erpnext_datev; do
  printf "%-16s " "$app:"; git -C apps/$app rev-parse HEAD
done
```

## ⚠️ Reproduzierbarkeits-Hinweise (bitte lesen)

`apps.json` pinnt auf **Branches**, nicht auf Commits. Branches bewegen sich – wer später
installiert, kann einen neueren Commit ziehen als wir (und ggf. noch höhere Runtime-
Anforderungen). Für exakte Reproduktion die Commits oben per `git checkout <hash>` fixieren.

**Backup-Inhalt:** Das mitgelieferte Backup (`20260710_224015-…`) enthält den
**vollständigen Demo-Datensatz** – Company (SKR04), beide Kunden, beide Artikel, die
Rechnungen RE-2026-0001 (*Paid*) und RE-2026-0002 (*Overdue*), die Zahlung, das Timesheet,
Steuervorlage 19 %, Bankkonto und den Dunning Type. Alternativ lässt sich der Datensatz per
`scripts/seed_demo.py` neu erzeugen (siehe README, Abschnitt „Alternative").
