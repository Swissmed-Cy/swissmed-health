import frappe
import datetime

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions

	conditions = get_event_conditions("Patient Appointment", filters)

	data = frappe.db.sql(
		"""
		select
		`tabPatient Appointment`.name, `tabPatient Appointment`.patient, `tabPatient Appointment`.service_unit,
		`tabPatient Appointment`.practitioner, `tabPatient Appointment`.status,
		`tabHealthcare Practitioner`.practitioner_name,
		`tabPatient Appointment`.duration,
		timestamp(`tabPatient Appointment`.appointment_date, `tabPatient Appointment`.appointment_time) as 'start',
		`tabAppointment Type`.color
		from
		`tabPatient Appointment`
		left join `tabAppointment Type` on `tabPatient Appointment`.appointment_type=`tabAppointment Type`.name
		left join `tabHealthcare Practitioner` on `tabPatient Appointment`.practitioner=`tabHealthcare Practitioner`.name
		where
		(`tabPatient Appointment`.appointment_date between %(start)s and %(end)s)
		and `tabPatient Appointment`.status != 'Cancelled' and `tabPatient Appointment`.docstatus < 2 {conditions}""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)

	for item in data:
		item.end = item.start + datetime.timedelta(minutes=item.duration)
		if item.practitioner_name:
			item.title = item.service_unit + " (" + item.patient + " with " + item.practitioner_name + ")"
		else:
			item.title = item.service_unit + " - " + item.patient

	return data

