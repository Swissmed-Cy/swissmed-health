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

@frappe.whitelist()
def get_room_numbers_by_therapy_types(therapy_type_ids):
    print(":::::::::::therapy_type_ids:::::::::::::",therapy_type_ids)
    if not therapy_type_ids:
        return []

    # Convert the comma-separated string of IDs into a list
    therapy_type_ids = therapy_type_ids.split(',')
    room_numbers = frappe.db.get_all('Total child rooms',
                                     filters={'parent': ['in', therapy_type_ids]},
                                     fields=['name1'])
    print(":::::::::room_numbers:::::::::::::::",room_numbers)

    sessions_rooms = []
    for room in room_numbers:
        sessions_rooms.append(room.get('name1'))
    return sessions_rooms

@frappe.whitelist()
def get_total_chair_by_therapy_types(therapy_type_ids):
    print(":::::::::::therapy_type_ids:::::::::::::",therapy_type_ids)
    if not therapy_type_ids:
        return []

    # Convert the comma-separated string of IDs into a list
    therapy_type_ids = therapy_type_ids.split(',')
    total_chair = frappe.db.get_all('Total Child Chair',
                                     filters={'parent': ['in', therapy_type_ids]},
                                     fields=['name1'])
    print(":::::::::total_chair:::::::::::::::",total_chair)

    sessions_rooms = []
    for chair in total_chair:
        sessions_rooms.append(chair.get('name1'))
    return sessions_rooms

@frappe.whitelist()
def get_total_beds_by_therapy_types11(therapy_type_ids):
    print(":::::::::::therapy_type_ids:::::::::::::",therapy_type_ids)
    if not therapy_type_ids:
        return []

    # Convert the comma-separated string of IDs into a list
    therapy_type_ids = therapy_type_ids.split(',')
    total_beds = frappe.db.get_all('Totals Beds Child',
                                     filters={'parent': ['in', therapy_type_ids]},
                                     fields=['totals_beds'])
    print(":::::::::total_beds:::::::::::::::",total_beds)

    sessions_rooms = []
    for bed in total_beds:
        sessions_rooms.append(bed.get('totals_beds'))
    return sessions_rooms

