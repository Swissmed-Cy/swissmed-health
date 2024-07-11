// File: frappe-bench/apps/your_app/your_app/public/js/therapy_session.js
frappe.ui.form.on('Therapy Session', {
    refresh: function(frm, cdt, cdn){
        apply_filters_for_chairs(frm, cdt, cdn)
        apply_filters_for_beds(frm, cdt, cdn)
        apply_filters_for_practitioner(frm, cdt, cdn)
        apply_filters_for_rooms(frm, cdt, cdn)
    },
    start_time: function(frm, cdt, cdn){
        apply_filters_for_chairs(frm, cdt, cdn)
        apply_filters_for_beds(frm, cdt, cdn)
        apply_filters_for_practitioner(frm, cdt, cdn)
    },
});

function apply_filters_for_chairs(frm, cdt, cdn){
    frm.set_query("custom_total_chairs", function(doc, cdt, cdn) {
        return {
            query: "swissmedhealth.swissmedhealth.customization.therapy_session.therapy_session.get_filterted_data",
            filters: {
                date: frm.doc.start_date,
                time: frm.doc.start_time,
                therapy_type: frm.doc.therapy_type,
                duration: frm.doc.duration,
                doc: "tabTotal Child Chair",
                custom_center_location: frm.doc.custom_center_location,
                field: "name1"
            }
        };
    });
}

function apply_filters_for_beds(frm, cdt, cdn){
    frm.set_query("custom_total_beds", function(doc, cdt, cdn) {
        return {
            query: "swissmedhealth.swissmedhealth.customization.therapy_session.therapy_session.get_filterted_data",
            filters: {
                date: frm.doc.start_date,
                time: frm.doc.start_time,
                therapy_type: frm.doc.therapy_type,
                duration: frm.doc.duration,
                doc: "tabTotals Beds Child",
                field: "totals_beds",
                custom_center_location: frm.doc.custom_center_location
            }
        };
    });
}

function apply_filters_for_practitioner(frm, cdt, cdn){
    frm.set_query("custom_practitioner", function(doc, cdt, cdn) {
        return {
            query: "swissmedhealth.swissmedhealth.customization.therapy_session.therapy_session.get_filterted_data",
            filters: {
                date: frm.doc.start_date,
                time: frm.doc.start_time,
                therapy_type: frm.doc.therapy_type,
                duration: frm.doc.duration,
                doc: "tabPractitioner",
                field: "name1"
            }
        };
    });
}

function apply_filters_for_rooms(frm, cdt, cdn){
    frm.set_query("custom_room_number_1", function(doc, cdt, cdn) {
        return {
            query: "swissmedhealth.swissmedhealth.customization.therapy_session.therapy_session.get_filterted_rooms",
            filters: {
                therapy_type: frm.doc.therapy_type,
                custom_center_location: frm.doc.custom_center_location
            }
        };
    });
}
