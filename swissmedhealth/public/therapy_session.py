import datetime
import json
from collections import OrderedDict
from datetime import datetime, timedelta
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
from datetime import datetime, timedelta


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
        `tabTherapy Session`.therapy_type,
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

    print ("\n data :::::::::::::", data)
    for item in data:
        item.end = item.start + timedelta(minutes=item.duration)  # Use timedelta correctly
        item.patient = item.patient + \
        '\n Start Time: ' + str(item.start) + \
        '\n Therapy PLAN: ' + item.name + '\n Practitioner:' + str(item.practitioner) + \
        '\n Therapy Type:' + str(item.therapy_type)
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
def get_total_beds_by_therapy_types(therapy_type_ids):
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

@frappe.whitelist()
def calculate_end_date(doc, method):
    if doc.start_date and doc.start_time and doc.duration:
        try:
            # Combine date and time into a single datetime object
            start_datetime_str = f"{doc.start_date} {doc.start_time}"
            start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M:%S")

            # Convert duration to minutes
            duration_minutes = float(doc.duration)

            # Calculate the end datetime by adding the duration to the start datetime
            end_datetime = start_datetime + timedelta(minutes=duration_minutes)

            # Set the calculated end_datetime to the custom_end_date field
            doc.custom_end_date = end_datetime

        except ValueError as e:
            frappe.throw(_("Invalid date/time format. Please enter a valid start date and time."))
    else:
        frappe.throw(_("Please ensure start date, start time, and duration are provided."))

# @frappe.whitelist()
# def validate_existing_session(session_name, start_datetime, custom_end_date, practitioner):
#     try:
#         # Convert string datetime to Python datetime objects
#         start_datetime = frappe.utils.data.parse_datetime(start_datetime)
#         custom_end_date = frappe.utils.data.parse_datetime(custom_end_date)

#         # Check if there are overlapping sessions for the same practitioner
#         overlapping_sessions = frappe.db.sql("""
#             SELECT name
#             FROM `tabTherapy Session`
#             WHERE practitioner = %s
#             AND (
#                 (%s BETWEEN start_datetime AND custom_end_date)
#                 OR (%s BETWEEN start_datetime AND custom_end_date)
#                 OR (start_datetime BETWEEN %s AND %s)
#             )
#             AND name != %s
#         """, (practitioner, start_datetime, custom_end_date, start_datetime, custom_end_date, session_name))

#         if overlapping_sessions:
#             return True  # There are overlapping sessions
#         else:
#             return False  # No overlapping sessions

#     except Exception as e:
#         frappe.log_error(f"Error in validate_existing_session: {e}", _("Validation Error"))
#         return True  # Return True to prevent submission in case of error
