# -*- coding: utf-8 -*-
# Seed der Testdaten laut docs/Testdaten-und-Einpflege-Anleitung.md
# Läuft im bench-console-Kontext (frappe schon initialisiert & verbunden).
import frappe
from frappe.utils import flt

frappe.set_user("Administrator")
frappe.flags.mute_emails = True

COMPANY    = "Facility- & Depotcleaning GmbH"
INCOME     = "4400 - Erlöse 19 % USt - F&DG"
RECEIVABLE = "1200 - Forderungen aus Lieferungen und Leistungen - F&DG"
TAX_ACC    = "3806 - Umsatzsteuer 19 % - F&DG"
BANK_GL    = "1800 - Bank - F&DG"
CC         = "Haupt - F&DG"

log = []
def ok(msg):   log.append("OK   " + msg); print("OK   " + msg)
def skip(msg): log.append("SKIP " + msg); print("SKIP " + msg)
def err(msg):  log.append("ERR  " + msg); print("ERR  " + msg)

def get_or_new(dt, name):
    if frappe.db.exists(dt, name):
        return frappe.get_doc(dt, name), True
    d = frappe.new_doc(dt)
    return d, False

# ---------------------------------------------------------------- 0 Company Tax ID + Adresse
try:
    comp = frappe.get_doc("Company", COMPANY)
    if not comp.tax_id:
        comp.tax_id = "DE123456789"
        comp.save(ignore_permissions=True)
        ok("Company Tax ID = DE123456789 gesetzt")
    else:
        skip("Company Tax ID bereits gesetzt")
    if not frappe.db.exists("Address", {"address_title": "FDC Firmensitz"}):
        a = frappe.new_doc("Address")
        a.address_title = "FDC Firmensitz"
        a.address_type = "Billing"
        a.address_line1 = "Lagerstraße 12"
        a.city = "Berlin"; a.pincode = "10115"; a.country = "Germany"
        a.email_id = "rechnung@fd-cleaning.example.de"
        a.is_your_company_address = 1
        a.append("links", {"link_doctype": "Company", "link_name": COMPANY})
        a.insert(ignore_permissions=True)
        ok("Company-Adresse (Lagerstraße 12) + E-Mail angelegt")
    else:
        skip("Company-Adresse existiert")
except Exception as e:
    err("Company/Adresse: %s" % e)

# ---------------------------------------------------------------- 1 Steuervorlage 19 %
TAXTPL = None
try:
    existing = frappe.get_all("Sales Taxes and Charges Template",
        filters={"title": "Umsatzsteuer 19 %", "company": COMPANY}, pluck="name")
    if existing:
        TAXTPL = existing[0]; skip("Steuervorlage 'Umsatzsteuer 19 %' existiert")
    else:
        t = frappe.new_doc("Sales Taxes and Charges Template")
        t.title = "Umsatzsteuer 19 %"; t.company = COMPANY
        t.append("taxes", {"charge_type": "On Net Total", "account_head": TAX_ACC,
                           "rate": 19, "description": "Umsatzsteuer 19 %"})
        t.insert(ignore_permissions=True)
        TAXTPL = t.name; ok(f"Steuervorlage 'Umsatzsteuer 19 %' angelegt ({t.name})")
except Exception as e:
    err("Steuervorlage: %s" % e)

# ---------------------------------------------------------------- 2 Bank + Bankkonto
try:
    if not frappe.db.exists("Bank", "Musterbank AG"):
        b = frappe.new_doc("Bank"); b.bank_name = "Musterbank AG"; b.insert(ignore_permissions=True)
        ok("Bank 'Musterbank AG' angelegt")
    else:
        skip("Bank existiert")
    if not frappe.db.exists("Bank Account", "Geschäftskonto FDC - Musterbank AG"):
        ba = frappe.new_doc("Bank Account")
        ba.account_name = "Geschäftskonto FDC"; ba.bank = "Musterbank AG"
        ba.is_company_account = 1; ba.company = COMPANY
        ba.account = BANK_GL; ba.iban = "DE89370400440532013000"
        ba.insert(ignore_permissions=True)
        ok("Bank Account 'Geschäftskonto FDC' (IBAN) angelegt -> %s" % ba.name)
    else:
        skip("Bank Account existiert")
except Exception as e:
    err("Bank/Bankkonto: %s" % e)

# ---------------------------------------------------------------- 3 Payment Terms
try:
    if not frappe.db.exists("Payment Term", "Netto 14 Tage"):
        pt = frappe.new_doc("Payment Term")
        pt.payment_term_name = "Netto 14 Tage"; pt.invoice_portion = 100
        pt.due_date_based_on = "Day(s) after invoice date"; pt.credit_days = 14
        pt.insert(ignore_permissions=True)
        ok("Payment Term 'Netto 14 Tage' angelegt")
    else:
        skip("Payment Term existiert")
    if not frappe.db.exists("Payment Terms Template", "Netto 14 Tage"):
        ptt = frappe.new_doc("Payment Terms Template")
        ptt.template_name = "Netto 14 Tage"
        ptt.append("terms", {"payment_term": "Netto 14 Tage", "invoice_portion": 100,
            "due_date_based_on": "Day(s) after invoice date", "credit_days": 14,
            "description": "Netto 14 Tage"})
        ptt.insert(ignore_permissions=True)
        ok("Payment Terms Template 'Netto 14 Tage' angelegt")
    else:
        skip("Payment Terms Template existiert")
except Exception as e:
    err("Payment Terms: %s" % e)

# ---------------------------------------------------------------- 4 Kunden + Adresse + Kontakt
def make_customer(name, group, tax_id, profile, buyer_ref, email, addr_line, city, pin,
                  contact_first, contact_last):
    try:
        if not frappe.db.exists("Customer", name):
            c = frappe.new_doc("Customer")
            c.customer_name = name; c.customer_type = "Company"
            c.customer_group = group; c.territory = "Germany"
            c.payment_terms = "Netto 14 Tage"
            if tax_id: c.tax_id = tax_id
            if frappe.get_meta("Customer").has_field("einvoice_profile"):
                c.einvoice_profile = profile
            if buyer_ref and frappe.get_meta("Customer").has_field("buyer_reference"):
                c.buyer_reference = buyer_ref
            if frappe.get_meta("Customer").has_field("electronic_address"):
                c.electronic_address = email
            c.insert(ignore_permissions=True)
            ok("Kunde '%s' angelegt (Profil %s)" % (name, profile))
        else:
            skip("Kunde '%s' existiert" % name)
        # Adresse
        atitle = name + " Rechnung"
        if not frappe.db.exists("Address", {"address_title": atitle}):
            a = frappe.new_doc("Address")
            a.address_title = atitle; a.address_type = "Billing"
            a.address_line1 = addr_line; a.city = city; a.pincode = pin; a.country = "Germany"
            a.email_id = email
            a.append("links", {"link_doctype": "Customer", "link_name": name})
            a.insert(ignore_permissions=True)
            ok("  Adresse für '%s' angelegt" % name)
        # Kontakt
        if not frappe.db.exists("Contact", {"first_name": contact_first, "last_name": contact_last}):
            ct = frappe.new_doc("Contact")
            ct.first_name = contact_first; ct.last_name = contact_last
            ct.append("email_ids", {"email_id": email, "is_primary": 1})
            ct.append("links", {"link_doctype": "Customer", "link_name": name})
            ct.insert(ignore_permissions=True)
            ok("  Kontakt %s %s angelegt" % (contact_first, contact_last))
    except Exception as e:
        err("Kunde %s: %s" % (name, e))

make_customer("Nordlicht Logistik GmbH", "Commercial", "DE811234567", "EN 16931", "",
              "buchhaltung@nordlicht-logistik.example.de", "Hafenweg 8", "Hamburg", "20457",
              "Petra", "Hansen")
make_customer("Landesamt für Liegenschaften Berlin", "Government", "", "XRECHNUNG",
              "04011000-1234512345-06", "rechnungseingang@lfl-berlin.example.de",
              "Behrenstraße 44", "Berlin", "10117", "Jonas", "Weber")

# ---------------------------------------------------------------- 5 Artikel + Preis
def make_item(code, iname, uom, rate):
    try:
        if not frappe.db.exists("Item", code):
            it = frappe.new_doc("Item")
            it.item_code = code; it.item_name = iname; it.item_group = "Services"
            it.stock_uom = uom; it.is_stock_item = 0; it.is_sales_item = 1
            it.append("item_defaults", {"company": COMPANY, "income_account": INCOME,
                                        "selling_cost_center": CC})
            it.insert(ignore_permissions=True)
            ok("Artikel %s '%s' angelegt" % (code, iname))
        else:
            skip("Artikel %s existiert" % code)
        if not frappe.db.exists("Item Price", {"item_code": code, "price_list": "Standard Selling"}):
            ip = frappe.new_doc("Item Price")
            ip.item_code = code; ip.price_list = "Standard Selling"; ip.selling = 1
            ip.price_list_rate = rate
            ip.insert(ignore_permissions=True)
            ok("  Verkaufspreis %s = %s €" % (code, rate))
    except Exception as e:
        err("Artikel %s: %s" % (code, e))

make_item("DL-001", "Unterhaltsreinigung", "Hour", 35)
make_item("DL-002", "Unterhaltsreinigung – Monatspauschale", "Nos", 1200)

# ---------------------------------------------------------------- 6 Employee + Activity + Timesheet
EMP = None
try:
    if not frappe.db.exists("Activity Type", "Unterhaltsreinigung"):
        at = frappe.new_doc("Activity Type"); at.activity_type = "Unterhaltsreinigung"
        at.insert(ignore_permissions=True); ok("Activity Type 'Unterhaltsreinigung' angelegt")
    else:
        skip("Activity Type existiert")
    existing_emp = frappe.get_all("Employee", filters={"employee_name": "Max Bergmann"}, pluck="name")
    if existing_emp:
        EMP = existing_emp[0]; skip("Employee 'Max Bergmann' existiert")
    else:
        e = frappe.new_doc("Employee")
        e.first_name = "Max"; e.last_name = "Bergmann"; e.gender = "Male"
        e.date_of_birth = "1985-05-20"; e.date_of_joining = "2026-01-01"
        e.status = "Active"; e.company = COMPANY
        e.insert(ignore_permissions=True); EMP = e.name
        ok("Employee 'Max Bergmann' angelegt -> %s" % EMP)
except Exception as e:
    err("Employee/Activity: %s" % e)

try:
    if EMP and not frappe.get_all("Timesheet", filters={"employee": EMP}, limit=1):
        ts = frappe.new_doc("Timesheet")
        ts.company = COMPANY; ts.employee = EMP
        for day in ["2026-06-03", "2026-06-10", "2026-06-17", "2026-06-24"]:
            ts.append("time_logs", {"activity_type": "Unterhaltsreinigung",
                "from_time": day + " 08:00:00", "hours": 8, "is_billable": 1,
                "billing_hours": 8, "billing_rate": 35})
        ts.insert(ignore_permissions=True); ts.submit()
        ok("Timesheet (4x8h billable, 1120 €) angelegt & gebucht -> %s" % ts.name)
    else:
        skip("Timesheet existiert oder kein Employee")
except Exception as e:
    err("Timesheet: %s" % e)

# ---------------------------------------------------------------- 7/8 Rechnungen
def make_invoice(target, customer, posting, due, item, qty, rate, profile, buyer_ref):
    try:
        if frappe.db.exists("Sales Invoice", target):
            skip("Rechnung %s existiert" % target)
            return frappe.get_doc("Sales Invoice", target)
        inv = frappe.new_doc("Sales Invoice")
        inv.naming_series = "ACC-SINV-.YYYY.-"
        inv.customer = customer; inv.company = COMPANY
        inv.posting_date = posting; inv.set_posting_time = 1; inv.due_date = due
        inv.debit_to = RECEIVABLE
        if frappe.get_meta("Sales Invoice").has_field("einvoice_profile"):
            inv.einvoice_profile = profile
        if buyer_ref and frappe.get_meta("Sales Invoice").has_field("buyer_reference"):
            inv.buyer_reference = buyer_ref
        inv.append("items", {"item_code": item, "qty": qty, "rate": rate,
            "income_account": INCOME, "cost_center": CC})
        inv.append("taxes", {"charge_type": "On Net Total", "account_head": TAX_ACC,
            "rate": 19, "description": "Umsatzsteuer 19 %"})
        inv.flags.name_set = True
        inv.name = target
        inv.insert(ignore_permissions=True)
        if inv.name != target:
            frappe.rename_doc("Sales Invoice", inv.name, target, force=True)
            inv = frappe.get_doc("Sales Invoice", target)
        inv.submit()
        ok("Rechnung %s gebucht: netto %s / brutto %s" % (target, inv.net_total, inv.grand_total))
        return inv
    except Exception as e:
        err("Rechnung %s: %s" % (target, e))
        return None

invA = make_invoice("RE-2026-0001", "Nordlicht Logistik GmbH", "2026-07-01", "2026-07-15",
                    "DL-001", 32, 35, "EN 16931", "")
invB = make_invoice("RE-2026-0002", "Landesamt für Liegenschaften Berlin", "2026-06-15",
                    "2026-06-29", "DL-002", 1, 1200, "XRECHNUNG", "04011000-1234512345-06")

# Zahlung für Rechnung A -> Paid
try:
    if frappe.db.exists("Sales Invoice", "RE-2026-0001"):
        siA = frappe.get_doc("Sales Invoice", "RE-2026-0001")
        if flt(siA.outstanding_amount) > 0:
            from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry
            pe = get_payment_entry("Sales Invoice", "RE-2026-0001")
            pe.posting_date = "2026-07-06"
            pe.reference_no = "RE-2026-0001"; pe.reference_date = "2026-07-06"
            pe.mode_of_payment = "Wire Transfer"; pe.paid_to = BANK_GL
            pe.insert(ignore_permissions=True); pe.submit()
            ok("Zahlung 1332,80 € gebucht -> RE-2026-0001 = Paid")
        else:
            skip("RE-2026-0001 bereits bezahlt")
except Exception as e:
    err("Payment Entry: %s" % e)

# Rechnung B -> Overdue erzwingen
try:
    if frappe.db.exists("Sales Invoice", "RE-2026-0002"):
        siB = frappe.get_doc("Sales Invoice", "RE-2026-0002")
        siB.set_status(update=True)
        siB.reload()
        ok("RE-2026-0002 Status = %s" % siB.status)
except Exception as e:
    err("Status RE-2026-0002: %s" % e)

# ---------------------------------------------------------------- 9 Dunning Type (+ Dunning best effort)
MAHNTEXT = ("Sehr geehrte Damen und Herren,\n"
            "zu der unten aufgeführten Rechnung konnten wir bis heute keinen Zahlungseingang "
            "feststellen. Wir bitten Sie, den offenen Betrag zuzüglich der ausgewiesenen "
            "Mahngebühr innerhalb von 7 Tagen auf das genannte Konto zu überweisen.")
try:
    if not frappe.db.exists("Dunning Type", "Erste Mahnung"):
        dt = frappe.new_doc("Dunning Type")
        dt.dunning_type = "Erste Mahnung"; dt.company = COMPANY; dt.is_default = 1
        dt.dunning_fee = 5; dt.rate_of_interest = 9.12
        dt.income_account = "4830 - Sonstige betriebliche Erträge - F&DG"
        dt.cost_center = CC
        try:
            dt.append("dunning_letter_text", {"language": "de", "body_text": MAHNTEXT,
                "closing_text": "Mit freundlichen Grüßen\nFacility- & Depotcleaning GmbH"})
        except Exception:
            pass
        dt.insert(ignore_permissions=True)
        ok("Dunning Type 'Erste Mahnung' (5 € / 9,12 %) angelegt")
    else:
        skip("Dunning Type existiert")
except Exception as e:
    err("Dunning Type: %s" % e)

# ---------------------------------------------------------------- 10 BIC + Standard-Bankkonto
BANKACC = "Geschäftskonto FDC - Musterbank AG"
try:
    bk = frappe.get_doc("Bank", "Musterbank AG")
    if not bk.get("swift_number"):
        bk.swift_number = "COBADEFFXXX"; bk.save(ignore_permissions=True)
        ok("BIC 'COBADEFFXXX' an Bank gesetzt")
    else:
        skip("BIC bereits gesetzt")
    if frappe.db.exists("Bank Account", BANKACC):
        ba = frappe.get_doc("Bank Account", BANKACC)
        if not ba.is_default:
            ba.is_default = 1; ba.save(ignore_permissions=True); ok("Bank Account als Standard markiert")
        else:
            skip("Bank Account bereits Standard")
except Exception as e:
    err("BIC/Standardkonto: %s" % e)

# ---------------------------------------------------------------- 11 Bank Transactions (Prozess 2)
try:
    if frappe.db.count("Bank Transaction") > 0:
        skip("Bank Transactions existieren bereits")
    elif frappe.db.exists("Bank Account", BANKACC):
        pe = frappe.get_all("Payment Entry", filters={"docstatus": 1},
            or_filters=[["paid_amount", "=", 1332.8]], pluck="name")
        pe = pe[0] if pe else None
        # Zeile 1: 1.332,80 € -> matcht RE-2026-0001
        bt1 = frappe.new_doc("Bank Transaction")
        bt1.date = "2026-07-06"; bt1.bank_account = BANKACC; bt1.deposit = 1332.80
        bt1.currency = "EUR"; bt1.description = "Rechnung RE-2026-0001, Kd-Nr K-1001"
        bt1.reference_number = "RE-2026-0001"
        bt1.party_type = "Customer"; bt1.party = "Nordlicht Logistik GmbH"
        bt1.insert(ignore_permissions=True); bt1.submit()
        if pe:
            bt1.append("payment_entries", {"payment_document": "Payment Entry",
                "payment_entry": pe, "allocated_amount": 1332.80})
            bt1.save(ignore_permissions=True); bt1.reload()
            ok("Bank-Zeile 1 (1.332,80 €) + Zahlung verknuepft -> " + str(bt1.status))
        else:
            ok("Bank-Zeile 1 angelegt (keine Zahlung gefunden)")
        # Zeile 2: 250,00 € -> unzuordenbar
        bt2 = frappe.new_doc("Bank Transaction")
        bt2.date = "2026-07-07"; bt2.bank_account = BANKACC; bt2.deposit = 250.00
        bt2.currency = "EUR"; bt2.description = "Zahlung, vielen Dank"
        bt2.reference_number = "M. Kowalski"
        bt2.insert(ignore_permissions=True); bt2.submit(); bt2.reload()
        ok("Bank-Zeile 2 (250,00 € unzuordenbar) angelegt -> " + str(bt2.status))
except Exception as e:
    err("Bank Transactions: %s" % e)

frappe.db.commit()
print("\n==== ZUSAMMENFASSUNG ====")
for l in log: print(l)
print("Kunden:", frappe.db.count("Customer"), "| Artikel:", frappe.db.count("Item"),
      "| Rechnungen:", frappe.db.count("Sales Invoice"),
      "| Zahlungen:", frappe.db.count("Payment Entry"))
