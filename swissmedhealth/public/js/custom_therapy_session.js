// frappe.ui.form.on('Therapy Session', {
//     refresh: function(frm) {
//         console.log("Testttttttttttttttttttttttt", frm.doc.custom_total_chairs)
//         // Ensure all required fields are filled
//         if (frm.doc.custom_total_chairs && frm.doc.practitioner && frm.doc.start_date && frm.doc.start_time && frm.doc.duration) {
//             // Calculate custom_end_date based on start_date, start_time, and duration
//             let start_datetime_str = `${frm.doc.start_date} ${frm.doc.start_time}`;
//             let start_datetime = new Date(start_datetime_str);
//             let duration_minutes = parseFloat(frm.doc.duration);

//             if (!isNaN(duration_minutes)) {
//                 // Calculate end datetime by adding duration to start datetime
//                 let end_datetime = new Date(start_datetime.getTime() + duration_minutes * 60000);
//                 frm.doc.custom_end_date = end_datetime.toISOString().slice(0, 19).replace('T', ' ');
//             }

//             // Asynchronous call handling: prevent immediate form submission
//             frappe.validated = false;

//             // Check chair booking
//             frappe.call({
//                 method: "frappe.client.get_list",
//                 args: {
//                     doctype: "Therapy Session",
//                     fields: ["name"],
//                     filters: [
//                         ["custom_total_chairs", "=", frm.doc.custom_total_chairs],
//                         ["start_date", "<=", frm.doc.custom_end_date],
//                         ["custom_end_date", ">=", frm.doc.start_date + ' ' + frm.doc.start_time],
//                         ["name", "!=", frm.doc.name]
//                     ]
//                 },
//                 callback: function(r) {
//                     if (r.message.length > 0) {
//                         frappe.msgprint(__('The selected chair is already booked. Please choose another chair or time slot.'));
//                         frappe.validated = false;
//                     } else {
//                         // If no chair conflict, check practitioner booking
//                         frappe.call({
//                             method: "frappe.client.get_list",
//                             args: {
//                                 doctype: "Therapy Session",
//                                 fields: ["name"],
//                                 filters: [
//                                     ["practitioner", "=", frm.doc.practitioner],
//                                     ["start_date", "<=", frm.doc.custom_end_date],
//                                     ["custom_end_date", ">=", frm.doc.start_date + ' ' + frm.doc.start_time],
//                                     ["name", "!=", frm.doc.name]
//                                 ]
//                             },
//                             callback: function(r) {
//                                 if (r.message.length > 0) {
//                                     frappe.msgprint(__('The selected practitioner is already booked. Please choose another practitioner or time slot.'));
//                                     frappe.validated = false;
//                                 } else {
//                                     // If no conflicts, proceed to update the chair status to "Booked"
//                                     frappe.call({
//                                         method: "frappe.client.get_list",
//                                         args: {
//                                             doctype: "Total Child Chair", // Ensure this is the correct doctype for chairs
//                                             name: frm.doc.custom_total_chairs,
//                                             fieldname: "status",
//                                             value: "Booked"
//                                         },
//                                         callback: function(r) {
//                                             if (!r.exc) {
//                                                 console.log("Chair status updated to Booked");
//                                                 // Set validated to true to allow form submission
//                                                 frappe.validated = true;
//                                                 frm.save(); // Save the form manually to proceed with submission
//                                             } else {
//                                                 console.error("Failed to update chair status");
//                                                 frappe.validated = false;
//                                             }
//                                         }
//                                     });
//                                 }
//                             }
//                         });
//                     }
//                 }
//             });
//         } else {
//             frappe.msgprint(__('Please fill in the chair, practitioner, start date, start time, and duration fields.'));
//             frappe.validated = false;
//         }
//     }
// });


// // frappe.ui.form.on('Therapy Session', {
// //     before_submit: function(frm,session_name, start_datetime, custom_end_date, practitioner) {
// //         console.log("::::::::::::::::::::tststs::::::::::::::::::");
// //         // Check if there are overlapping sessions for the same practitioner
// //         frappe.call({
// //             method: "validate_existing_session",
// //             args: {
// //                 session_name: frm.doc.name,
// //                 start_datetime: frm.doc.start_date + ' ' + frm.doc.start_time,
// //                 custom_end_date: frm.doc.custom_end_date,
// //                 practitioner: frm.doc.practitioner
// //             },
// //             callback: function(r) {
// //                 if (r.message) {
// //                     frappe.msgprint(__('The selected practitioner is already booked for this time slot. Please choose another time slot.'));
// //                     frappe.validated = false;
// //                 } else {
// //                     frappe.validated = true;
// //                     frm.save(); // Save the form manually to proceed with submission
// //                 }
// //             }
// //         });
// //     }
// // });
