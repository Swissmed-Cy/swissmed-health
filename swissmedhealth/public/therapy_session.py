import datetime
import json
from collections import OrderedDict

import frappe
from frappe import _, bold
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder import Criterion
from frappe.query_builder.functions import IfNull, Max, Min
from frappe.utils import (
	add_days,
	add_to_date,
	cint,
	flt,
	get_datetime,
	get_link_to_form,
	get_time,
	getdate,
	time_diff,
	time_diff_in_hours,
	time_diff_in_seconds,
)


@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	print ("\n filters :::::::::::::::", start, end, filters)

	conditions = get_event_conditions("Therapy Session", filters)

	data = frappe.db.sql(
		"""
		select
		`tabTherapy Session`.name, `tabTherapy Session`.patient,
		`tabTherapy Session`.practitioner,
		`tabTherapy Session`.duration,
		timestamp(`tabTherapy Session`.start_date, `tabTherapy Session`.start_time) as 'start'
		from
		`tabTherapy Session`
		where
		(`tabTherapy Session`.start_date between %(start)s and %(end)s)
		and `tabTherapy Session`.docstatus < 2 {conditions}""".format(
			conditions=conditions
		),
		{"start": start, "end": end},
		as_dict=True,
		update={"allDay": 0},
	)

	for item in data:
		item.end = item.start + datetime.timedelta(minutes=item.duration)

	return data