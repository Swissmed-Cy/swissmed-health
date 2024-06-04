// Copyright (c) 2024, KAINOTOMO PH LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on("Patient Treatment Plan", {
	master_category(frm) {
		if(frm.doc.master_category == "Treatment"){
			frm.set_value("naming_series",'TR')
		}else{
			frm.set_value("naming_series",'CN')
		}
	}
});


frappe.ui.form.on('Patient Treatment Plan', {
    end_date: function(frm) {
        calculate_duration(frm);
    },
    start_date: function(frm) {
        calculate_duration(frm);
    }
});

function calculate_duration(frm) {
    if (frm.doc.start_date && frm.doc.end_date) {
        let start = moment(frm.doc.start_date);
        let end = moment(frm.doc.end_date);
        let duration = moment.duration(end.diff(start));
        let minutes = duration.asMinutes();
        frm.set_value('duration', minutes);
    }
}

frappe.ui.form.on('Patient Treatment Plan', {
    before_submit: function(frm) {
        if (frm.doc.room) {
            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Room Number",
                    name: frm.doc.room,
                    fieldname: "status",
                    value: "Booked"
                },
                callback: function(r) {
                    if (!r.exc) {
                        console.log("Room status updated to Booked");
                    } else {
                        console.error("Failed to update room status");
                    }
                }
            });
        }
    }
});


frappe.ui.form.on('Patient Treatment Plan', {
    validate: function(frm) {
        if (frm.doc.room && frm.doc.start_date && frm.doc.end_date) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Patient Treatment Plan",
                    fields: ["name"],
                    filters: [
                        ["room", "=", frm.doc.room],
                        ["start_date", "<", frm.doc.end_date],
                        ["end_date", ">", frm.doc.start_date],
                        ["name", "!=", frm.doc.name]
                    ]
                },
                callback: function(r) {
                    if (r.message.length > 0) {
                        frappe.msgprint(__('The selected room is already booked for the specified time slot. Please choose another room or time slot.'));
                        frappe.validated = false;
                    } else {
                        frappe.call({
                            method: "frappe.client.set_value",
                            args: {
                                doctype: "Room Number",
                                name: frm.doc.room,
                                fieldname: "status",
                                value: "Booked"
                            },
                            callback: function(r) {
                                if (!r.exc) {
                                    console.log("Room status updated to Booked");
                                } else {
                                    console.error("Failed to update room status");
                                }
                            }
                        });
                    }
                }
            });
        }
    }
});
