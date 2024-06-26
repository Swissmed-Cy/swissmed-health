frappe.ui.form.on('Quotation', {
    refresh: function(frm) {
        if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Create Therapy Plan'), function() {
                create_therapy_plan(frm);
            }, __('Create')); // Adding under 'Actions' instead of 'Create'
        }
    }
});

function create_therapy_plan(frm) {
    frappe.call({
        method: 'swissmedhealth.swissmedhealth.hooks.quotation.create_therapy_plan',
        args: {
            quotation_name: frm.doc.name
        },
        callback: function(r) {
            if (!r.exc) {
                frappe.msgprint(__('Therapy Plan created successfully'));
                frappe.set_route('Form', 'Therapy Plan', r.message);
            }
        }
    });
}
