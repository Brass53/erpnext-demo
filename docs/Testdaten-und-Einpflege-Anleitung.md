# ERPNext Demo – Konkreter Testdatensatz & Einpflege-Anleitung

**Team Scrumateure · Stand: 10.07.2026**

Dieses Dokument setzt die Testdaten-Spezifikation in einen konkreten, in sich konsistenten Datensatz um. Alle 🔒-Anker aus der Spezifikation sind erfüllt und prozessübergreifend abgestimmt. Die Werte müssen nur noch in ERPNext eingetragen werden – **in der Reihenfolge der Anleitung in Teil B**, da spätere Schritte auf früheren aufbauen.

> **Wichtigster Zusammenhang (nicht verändern):**
> Stundensatz 35,00 € × 32 h = **1.120,00 € netto** → + 19 % USt (212,80 €) = **1.332,80 € brutto Rechnung A** = **Betrag Bank-Zeile 1**, und die Rechnungsnummer **RE-2026-0001** steht im Verwendungszweck von Zeile 1. Wer einen Wert ändert, muss die ganze Kette anpassen.

---

# Teil A – Der Testdatensatz

## A.1 Verkäufer / Company-Stammdaten

| Feld | Wert |
|---|---|
| Firmenname | **Facility- & Depotcleaning GmbH** |
| Abkürzung (ERPNext) | FDC |
| Anschrift | Lagerstraße 12, 10115 Berlin, Deutschland |
| USt-IdNr. (Tax ID) | DE123456789 |
| Steuernummer | 30/222/50712 |
| IBAN | DE89 3704 0044 0532 0130 00 |
| BIC | COBADEFFXXX |
| Bankname | Musterbank AG |
| E-Mail (BT-34) | rechnung@fd-cleaning.example.de |
| Handelsregister | HRB 198765 B, Amtsgericht Charlottenburg |
| Kontenrahmen | **SKR04** (mit Kontonummern) |
| Steuervorlage Ausgang | **Umsatzsteuer 19 %** (SKR04-Konto 3806) |
| Geschäftsjahr | **01.01.2026 – 31.12.2026** |

Hinweis: Die IBAN ist eine format-gültige Standard-Test-IBAN, die USt-IdNr. ist format-gültig (DE + 9 Ziffern, erfüllt BR-DE-2), aber nicht real vergeben – für die Demo ausreichend, für Echtbetrieb ersetzen.

## A.2 Kunden

### Kunde A – „läuft glatt" (B2B → ZUGFeRD)

| Feld | Wert |
|---|---|
| Kundenname | Nordlicht Logistik GmbH |
| Kundennummer | K-1001 |
| Anschrift | Hafenweg 8, 20457 Hamburg, Deutschland |
| USt-IdNr. | DE811234567 |
| E-Mail (BT-49) | buchhaltung@nordlicht-logistik.example.de |
| Ansprechpartner | Frau Petra Hansen (Leitung Buchhaltung) |
| Rechnungsform | **ZUGFeRD (EN-16931-Profil, PDF + XML)** |
| Leitweg-ID | – (nicht nötig, B2B) |
| Zahlungsziel | **Netto 14 Tage** |
| Rolle | Rechnung aus Timesheet, wird bezahlt → Status **Paid** |

### Kunde B – „Mahnfall" (B2G → XRechnung)

| Feld | Wert |
|---|---|
| Kundenname | Landesamt für Liegenschaften Berlin |
| Kundennummer | K-1002 |
| Anschrift | Behrenstraße 44, 10117 Berlin, Deutschland |
| USt-IdNr. | – (Behörde, nicht erforderlich) |
| E-Mail (BT-49) | rechnungseingang@lfl-berlin.example.de |
| Ansprechpartner | Herr Jonas Weber (Rechnungsstelle) |
| Rechnungsform | **XRechnung 3.0.2 (reines XML)** |
| Leitweg-ID (BT-10) | **04011000-1234512345-06** |
| Zahlungsziel | **Netto 14 Tage** |
| Rolle | Pauschalrechnung, bleibt unbezahlt → Status **Overdue**, Mahnlauf |

Die Leitweg-ID ist das offizielle Beispiel aus der KoSIT-Spezifikation – format-gültig inkl. Prüfziffer, ideal für die Demo. Eine echte ID vergibt nur der Auftraggeber.

## A.3 Artikel & Steuer

### Item 1: Unterhaltsreinigung (Stundenabrechnung, Kunde A)

| Feld | Wert |
|---|---|
| Item-Code / Name | DL-001 / Unterhaltsreinigung |
| Item-Typ | Dienstleistung → **Maintain Stock = Nein** |
| Einheit (UOM) | **Stunde** – UN/ECE-Code **HUR** |
| Stundensatz (Verkaufspreis) | **35,00 € netto** |
| Erlöskonto | 4400 – Erlöse 19 % USt (SKR04) |
| Steuer | 19 % |

### Item 2: Unterhaltsreinigung Pauschale (Monatspauschale, Kunde B)

| Feld | Wert |
|---|---|
| Item-Code / Name | DL-002 / Unterhaltsreinigung – Monatspauschale |
| Item-Typ | Dienstleistung → Maintain Stock = Nein |
| Einheit (UOM) | Stück (C62) oder Monat |
| Monatsbetrag | **1.200,00 € netto** |
| Erlöskonto | 4400 – Erlöse 19 % USt (SKR04) |
| Steuer | 19 % |

## A.4 Zeiterfassung (Prozess 1)

| Feld | Wert |
|---|---|
| Mitarbeiter | Max Bergmann (Personalnr. MA-001, Objektleiter Reinigung) |
| Activity Type | Unterhaltsreinigung (Billing aktiv, Billing Rate 35,00 €) |
| Timesheet-Zeitraum | Juni 2026 |
| Erfasste Stunden Kunde A | **32,0 h**, abrechenbar (Billable) |

Beispiel-Aufteilung der 32 h (frei anpassbar, Summe muss 32 h bleiben):

| Datum | Stunden |
|---|---|
| 03.06.2026 | 8,0 |
| 10.06.2026 | 8,0 |
| 17.06.2026 | 8,0 |
| 24.06.2026 | 8,0 |

**Rechenregel:** 32 h × 35,00 € = **1.120,00 € netto** (= Netto Rechnung A).

## A.5 Rechnungen

### Rechnung A (aus Timesheet, Kunde A, ZUGFeRD)

| Feld | Wert |
|---|---|
| Rechnungsnummer | **RE-2026-0001** |
| Rechnungsdatum | 01.07.2026 |
| Leistungszeitraum (BT-72) | 01.06.2026 – 30.06.2026 |
| Fälligkeit | 15.07.2026 (14 Tage netto) |
| Position | 32 h × 35,00 € Unterhaltsreinigung |
| Netto | 1.120,00 € |
| 19 % USt | 212,80 € |
| **Brutto** | **1.332,80 €** |
| Ziel-Status | **Paid** (nach Bank-Import, Prozess 2) |

### Rechnung B (Pauschale, Kunde B, XRechnung)

| Feld | Wert |
|---|---|
| Rechnungsnummer | **RE-2026-0002** |
| Rechnungsdatum | 15.06.2026 (rückdatiert!) |
| Leistungszeitraum (BT-72) | 01.06.2026 – 30.06.2026 |
| Fälligkeit | **29.06.2026** (14 Tage netto → liegt in der Vergangenheit) |
| Position | 1 × 1.200,00 € Monatspauschale Juni |
| Netto | 1.200,00 € |
| 19 % USt | 228,00 € |
| **Brutto** | **1.428,00 €** |
| Ziel-Status | **Overdue**, bleibt unbezahlt → Mahnlauf |

## A.6 Bank-Daten (Prozess 2)

| Feld | Wert |
|---|---|
| Bank (ERPNext) | Musterbank AG |
| Bank Account | Geschäftskonto FDC – DE89 3704 0044 0532 0130 00 |

**Bank-CSV (2 Buchungen)** – liegt als fertige Datei `bank_import.csv` bei:

| Datum | Betrag | Verwendungszweck | Auftraggeber |
|---|---|---|---|
| 2026-07-06 | 1332.80 | Rechnung RE-2026-0001, Kd-Nr K-1001 | Nordlicht Logistik GmbH |
| 2026-07-07 | 250.00 | Zahlung, vielen Dank | M. Kowalski |

Zeile 1 = Brutto Rechnung A, Rechnungsnummer im Verwendungszweck → **matcht automatisch**.
Zeile 2 = kein Bezug zu einer Rechnung → **unzuordenbar, manueller Fall** (bleibt in der Demo offen bzw. wird manuell behandelt).
Kunde B bekommt bewusst **keine** Bankzeile.

## A.7 Mahnwesen (Prozess 3)

| Feld | Wert |
|---|---|
| Dunning Type | **Erste Mahnung** |
| Mahngebühr | **5,00 €** (fester Betrag) |
| Verzugszins | 9,12 % p. a. |
| Payment Terms Template | **Netto 14 Tage** (100 % fällig 14 Tage nach Rechnungsdatum) |

Mahntext-Vorschlag (anpassbar):

> Sehr geehrte Damen und Herren,
> zu der unten aufgeführten Rechnung konnten wir bis heute keinen Zahlungseingang feststellen. Wir bitten Sie, den offenen Betrag zuzüglich der ausgewiesenen Mahngebühr innerhalb von 7 Tagen auf das genannte Konto zu überweisen. Sollte sich Ihre Zahlung mit diesem Schreiben überschnitten haben, betrachten Sie diese Mahnung bitte als gegenstandslos.
> Mit freundlichen Grüßen
> Facility- & Depotcleaning GmbH

---

# Teil B – Anleitung: Einpflegen in ERPNext (Schritt für Schritt)

Die Reihenfolge ist verbindlich – Kunden brauchen das Payment-Terms-Template, Rechnungen brauchen Artikel und Kunden usw. Menübezeichnungen beziehen sich auf ERPNext v15; je nach Version/Sprache können sie leicht abweichen. Am schnellsten erreicht man jeden DocType über die Suchleiste oben (einfach z. B. „Customer" eintippen).

## Schritt 1: Company & Grundeinstellungen

1. Falls beim ersten Start der **Setup-Assistent** läuft: Land **Germany**, Währung EUR, Firmenname **Facility- & Depotcleaning GmbH**, Kontenplan **SKR04 mit Kontonummern** wählen. (Nachträglich: *Accounting → Chart of Accounts* prüfen, ob SKR04-Konten wie 4400 existieren.)
2. **Geschäftsjahr:** Suche → „Fiscal Year" → prüfen, ob **2026** (01.01.–31.12.2026) existiert, sonst neu anlegen.
3. **Company-Stammdaten:** Suche → „Company" → Facility- & Depotcleaning GmbH öffnen → **Tax ID** = DE123456789, Steuernummer, Telefon/E-Mail eintragen. Unter *Address & Contact* eine neue Adresse (Lagerstraße 12, 10115 Berlin, Germany) und die E-Mail rechnung@fd-cleaning.example.de anlegen.
4. **Steuervorlage:** Suche → „Sales Taxes and Charges Template" → prüfen/anlegen: **„Umsatzsteuer 19 %"**, Zeile: *On Net Total*, Konto **3806 Umsatzsteuer 19 %** (SKR04), Satz 19. Als Standard (Default) markieren.

## Schritt 2: Bank & Bankkonto

1. Suche → „Bank" → Neu: **Musterbank AG**.
2. Suche → „Bank Account" → Neu: Name „Geschäftskonto FDC", Bank = Musterbank AG, **Is Company Account = Ja**, Company auswählen, IBAN **DE89370400440532013000**, als *Company Bank Account* in der Company hinterlegen (Feld *Default Bank Account*).

Damit sind IBAN/BIC später automatisch in der X-Rechnung (Zahlungsanweisung) enthalten.

## Schritt 3: Payment Terms

1. Suche → „Payment Term" → Neu: **„Netto 14 Tage"**, Invoice Portion 100 %, Due Date Based On = *Day(s) after invoice date*, Credit Days = **14**.
2. Suche → „Payment Terms Template" → Neu: **„Netto 14 Tage"**, den eben erstellten Payment Term als einzige Zeile einfügen.

## Schritt 4: Kunden anlegen

Für **beide** Kunden (Werte aus A.2): Suche → „Customer" → Neu.

1. Kundenname eintragen, Customer Type = *Company*, Territory = Germany.
2. Reiter *Accounting*: **Payment Terms Template = Netto 14 Tage**.
3. Bei Kunde A: **Tax ID = DE811234567**.
4. Speichern, dann im Kundenformular **Adresse** (Billing) und **Kontakt** (Ansprechpartner + E-Mail) anlegen – die E-Mail des Kontakts ist die elektronische Käuferadresse (BT-49).
5. **eu_einvoice-Felder** (die App ergänzt Felder am Kunden bzw. an der Rechnung): bei Kunde A das E-Invoice-Format auf **ZUGFeRD**, bei Kunde B auf **XRechnung** stellen und bei Kunde B die **Leitweg-ID 04011000-1234512345-06** in das entsprechende Feld (Buyer Reference / Leitweg-ID) eintragen. Falls das Feld nur auf der Rechnung erscheint, wird es dort in Schritt 8 gesetzt.

## Schritt 5: Einheit & Artikel

1. **UOM prüfen:** Suche → „UOM" → „Stunde" (bzw. „Hour") muss existieren. Für die X-Rechnung muss die Einheit auf den UN/ECE-Code **HUR** gemappt sein – die eu_einvoice-App bringt ein Mapping für gängige Einheiten mit; falls ein Feld „Common Code"/„UNECE Code" an der UOM existiert, dort **HUR** eintragen.
2. **Item DL-001 Unterhaltsreinigung:** Suche → „Item" → Neu. Item Code DL-001, **Maintain Stock = Nein**, Default UOM = **Stunde**. Reiter *Sales*: Standard-Verkaufspreis **35,00 €** (legt einen Item Price in der Standard-Preisliste an). Reiter *Accounting*: Default Income Account = **4400** (SKR04). Item Tax: 19 %-Vorlage.
3. **Item DL-002 Monatspauschale:** analog, UOM Stück/Monat, Preis **1.200,00 €**, gleiches Erlöskonto.

## Schritt 6: Mitarbeiter, Activity Type, Timesheet (Prozess 1)

1. Suche → „Employee" → Neu: **Max Bergmann**, Company FDC, Status Active.
2. Suche → „Activity Type" → Neu: **Unterhaltsreinigung**. (Optional über „Activity Cost" die Billing Rate 35 € je Mitarbeiter hinterlegen – dann wird sie im Timesheet vorbefüllt.)
3. Suche → „Timesheet" → Neu: Employee = Max Bergmann. Vier Zeilen gemäß A.4 anlegen; in jeder Zeile: Activity Type = Unterhaltsreinigung, Stunden = 8, Haken **Billable**, **Billing Rate = 35,00 €**, Billing Hours = 8. **Wichtig:** Kunde/Projektbezug so wählen, dass die Zeiten Kunde A zugeordnet sind (Feld *Customer* im Timesheet-Detail bzw. über ein Projekt für Nordlicht Logistik).
4. Prüfen: Total Billable Amount = **1.120,00 €**. Dann **Submit**.

## Schritt 7: Rechnung A erstellen (ZUGFeRD)

1. Im abgeschlossenen Timesheet: Button **Create Sales Invoice** → Kunde **Nordlicht Logistik GmbH**, Item **DL-001** wählen.
2. In der Rechnung kontrollieren/setzen: **Posting Date 01.07.2026** (dazu ggf. „Edit Posting Date" aktivieren), Payment Terms = Netto 14 Tage → Due Date **15.07.2026**, Steuer-Vorlage 19 %, Menge 32 × 35,00 €.
3. **Leistungszeitraum (BT-72)** setzen: 01.06.–30.06.2026 – im von eu_einvoice ergänzten Feld (z. B. *Leistungsdatum/Leistungszeitraum*).
4. **Naming/Nummer:** Damit die Nummer **RE-2026-0001** lautet, vorab unter *Settings → Naming Series* für Sales Invoice die Serie **RE-2026-** anlegen und auswählen (sonst vergibt ERPNext ACC-SINV-…; die Demo funktioniert auch damit, dann muss aber der Verwendungszweck in der Bank-CSV auf die tatsächliche Nummer angepasst werden!).
5. Prüfen: Netto 1.120,00 / USt 212,80 / **Brutto 1.332,80 €** → **Submit**.
6. **ZUGFeRD erzeugen:** In der gebuchten Rechnung den von eu_einvoice bereitgestellten Button/Menüpunkt (z. B. *Download E-Invoice / ZUGFeRD-PDF*) nutzen. Ergebnis: PDF mit eingebettetem XML.

## Schritt 8: Rechnung B erstellen (XRechnung)

1. Suche → „Sales Invoice" → Neu: Kunde **Landesamt für Liegenschaften Berlin**.
2. **Posting Date 15.06.2026** (rückdatieren!), Payment Terms Netto 14 Tage → Due Date **29.06.2026**.
3. Position: 1 × **DL-002** Monatspauschale, 1.200,00 €, Steuer 19 % → Brutto **1.428,00 €**.
4. Leistungszeitraum 01.06.–30.06.2026 (BT-72) und – falls nicht schon am Kunden hinterlegt – **Leitweg-ID 04011000-1234512345-06** eintragen. Nummer: **RE-2026-0002**.
5. **Submit.** Die Rechnung ist zunächst *Unpaid*; da die Fälligkeit in der Vergangenheit liegt, setzt ERPNext den Status (spätestens nach dem nächtlichen Statuslauf, manuell erzwingbar durch Neuladen/Statusupdate) auf **Overdue**.
6. **XRechnung erzeugen:** Button der eu_einvoice-App → reines XML herunterladen. Validierung z. B. gegen den KoSIT-Validator möglich (für die Demo optional).

## Schritt 9: Bank-Import & Zahlungsabgleich (Prozess 2)

1. Beiliegende Datei **`bank_import.csv`** verwenden (Spalten: Datum, Betrag, Verwendungszweck, Auftraggeber – wie in A.6).
2. Suche → **„Bank Statement Import"** → Neu: Bank Account = Geschäftskonto FDC, CSV hochladen. Im Mapping-Schritt zuordnen: Datum → *Date*, Betrag → *Deposit*, Verwendungszweck → *Description* (und/oder *Reference Number*), Auftraggeber → *Party/Description*. Import starten → es entstehen 2 **Bank Transactions**.
3. Suche → **„Bank Reconciliation Tool"**: Bank Account und Zeitraum (01.07.–10.07.2026) wählen.
   - **Zeile 1 (1.332,80 €):** Über *Actions → Match Against Voucher* schlägt ERPNext die offene Rechnung RE-2026-0001 vor (Betrag identisch + Nummer im Verwendungszweck). Zuordnen → ERPNext erzeugt den **Payment Entry** → Rechnung A springt auf **Paid**. ✅
   - **Zeile 2 (250,00 €):** Es gibt keinen passenden Beleg – genau der gewollte **manuelle Fall**. Für die Demo: zeigen, dass kein Match vorgeschlagen wird; die Transaktion bleibt *Unreconciled* (alternativ manuell als „unzuordenbarer Zahlungseingang" auf ein Verrechnungskonto buchen und erläutern).
4. Kontrolle: Kunde B taucht im Banklauf **nicht** auf – Rechnung B bleibt offen.

## Schritt 10: Mahnlauf (Prozess 3)

1. Suche → **„Dunning Type"** → Neu: **„Erste Mahnung"**, Company FDC, **Dunning Fee = 5,00 €**, **Rate of Interest = 9,12 %**, Mahntext aus A.7 einfügen. Als Standard markieren.
2. Suche → **„Dunning"** → Neu: Customer = Landesamt für Liegenschaften Berlin → über **Fetch Overdue Payments** die überfällige Rechnung **RE-2026-0002** ziehen. ERPNext berechnet: 1.428,00 € offen + 5,00 € Mahngebühr (+ anteilige Verzugszinsen).
3. Dunning Type „Erste Mahnung" wählen, prüfen, **Submit** → Mahnung als **PDF drucken** (Print-Button) bzw. per E-Mail an den Ansprechpartner senden.

## Schritt 11: Konsistenz-Checkliste abhaken

- [ ] Brutto Rechnung A (1.332,80 €) == Betrag Bank-Zeile 1
- [ ] Rechnungsnummer A (RE-2026-0001) steht im Verwendungszweck von Zeile 1
- [ ] Rechnung B: Fälligkeit 29.06.2026 < heute → Status **Overdue**
- [ ] Bank-Zeile 2 (250,00 €) hat keine passende Rechnung → bleibt offen
- [ ] Kunde B hat keine Bank-Zeile
- [ ] Item-Einheit = Stunde mit UN/ECE-Code **HUR**
- [ ] Verkäufer hat USt-IdNr., IBAN und E-Mail (sonst X-Rechnung-Validierung rot)
- [ ] Leistungszeitraum (BT-72) auf **beiden** Rechnungen gesetzt
- [ ] Rechnungsform pro Kunde korrekt: A = ZUGFeRD (B2B), B = XRechnung + Leitweg-ID (B2G)

---

## Bekannte Stolpersteine (aus Erfahrung)

1. **Naming Series:** Ohne eigene Serie vergibt ERPNext ACC-SINV-2026-00001. Entweder vorher die Serie RE-2026- anlegen **oder** die tatsächliche Nummer in `bank_import.csv` (Verwendungszweck Zeile 1) nachziehen – sonst schlägt das Auto-Matching fehl.
2. **Rückdatierung Rechnung B:** Posting Date lässt sich nur ändern, wenn „Edit Posting Date/Time" aktiviert ist und das Datum im offenen Geschäftsjahr 2026 liegt.
3. **Overdue-Status** wird von einem täglichen Hintergrundjob gesetzt. Erscheint er nicht sofort: kurz warten oder im Docker-Container `bench execute erpnext.accounts.doctype.sales_invoice.sales_invoice.update_status` bzw. den Scheduler anstoßen – für die Demo reicht meist die Anzeige „Unpaid + Fälligkeit rot".
4. **eu_einvoice-Validierung rot?** Fast immer fehlt eines der Pflichtfelder aus Schritt 1–2: USt-IdNr., IBAN/Bankkonto, Verkäufer-E-Mail oder das Leistungsdatum.
