import frappe


def set_total_advance_paid(name):
	aple = frappe.qb.DocType("Advance Payment Ledger Entry")
	paid_amount_condition = aple.amount > 0
	return frappe.qb.from_(aple).where(paid_amount_condition).where(aple.name == name)
