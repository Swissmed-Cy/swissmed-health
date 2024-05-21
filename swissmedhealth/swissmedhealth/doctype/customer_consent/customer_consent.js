// Copyright (c) 2024, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Consent', {
	refresh: function (frm) {
		// if field acceptance_date is empty set the current date
		if (!frm.doc.acceptance_date) {
			frm.set_value("acceptance_date", frappe.datetime.nowdate());
		}
	}
});
