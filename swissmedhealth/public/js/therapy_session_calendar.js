
frappe.views.calendar["Therapy Session"] = {
	field_map: {
		"status": "status",
        "id": "name",
        "title": "patient",
        "start": "start",
        "end": "end",  // Make sure you have an end_date if needed
        // "allDay": "all_day", // Optional, if you are using all-day events
        "therapy_plan": "therapy_plan",
        "eventColor": "color"
	},
	order_by: "start_date",
	gantt: true,
	get_events_method: "swissmedhealth.public.therapy_session.get_events"
};
