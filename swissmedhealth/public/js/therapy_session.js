// File: frappe-bench/apps/your_app/your_app/public/js/therapy_session.js

frappe.ui.form.on('Therapy Session', {
    // refresh: function(frm) {
    //     frm.add_fetch('therapy_type', 'room_number', 'room_number');
    // },
    therapy_type: function(frm) {
        console.log("test :::::::::::::::::::::::::::::::::::");
        if(frm.doc.therapy_type) {
            // Fetch room numbers based on selected therapy types
            frappe.call({
                method: 'swissmedhealth.public.therapy_session.get_room_numbers_by_therapy_types',
                args: {
                    therapy_type_ids: frm.doc.therapy_type
                },
                callback: function(r) {
                    if(r.message) {
                        let room_numbers = r.message;
                        frm.clear_table("custom_room_number_1");  // Assuming "room_numbers" is the table field
                        
                        room_numbers.forEach(function(room) {
                            console.log("room ::::::::::::::::", room);
                            let new_row = frm.add_child("custom_room_number_1");
                            new_row.name1 = room;
                        });
                        
                        refresh_field("custom_room_number_1");
                    }
                }
            });
        }
    }
});


frappe.ui.form.on('Therapy Session', {
    therapy_type: function(frm) {
        console.log("test :::::::::::::::::::::::::::::::::::");
        if(frm.doc.therapy_type) {
            // Fetch room numbers based on selected therapy types
            frappe.call({
                method: 'swissmedhealth.public.therapy_session.get_total_chair_by_therapy_types',
                args: {
                    therapy_type_ids: frm.doc.therapy_type
                },
                callback: function(r) {
                    if(r.message) {
                        let chair_numbers = r.message;
                        frm.clear_table("custom_total_chairs");  // Assuming "room_numbers" is the table field
                        
                        chair_numbers.forEach(function(chair) {
                            console.log("chair ::::::::::::::::", chair);
                            let new_row = frm.add_child("custom_total_chairs");
                            new_row.name1 = chair;
                        });
                        
                        refresh_field("custom_total_chairs");
                    }
                }
            });
        }
    }
});
