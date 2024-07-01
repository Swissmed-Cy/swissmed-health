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

    # status_color_map = {
    #     "Draft": "#0000FF",    # Blue
    #     "Submitted": "#00FF00", # Green
    #     "Cancelled": "FF0000"  # Red
    # }
    #Initialize conditions
    # conditions = "1=1"
    # if filters:
    #     filters = json.loads(filters)
    #     if filters.get("docstatus"):
    #         conditions += f" AND `tabTherapy Session`.docstatus = '{filters['document_status']}'"


    
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
    
    for session in data:
        session['total_child_rooms'] = frappe.db.sql(
            """
            select
                name1 
            from
                `tabTotal child rooms`
            where
                parent = %s
            """,
            session['name'],
            as_dict=True
        )
  
    print ("\n data ::::Before:::::::::", data)

    #Map the status to colors
    # for session in data:
    #     session['color'] = status_color_map.get(session.get('docstatus'), "#0000FF")  # Default color if status not in map
    
    for item in data:
        print (" item custom room no :::::",item)
        room_numbers = [i.get('name1') for i in item.get('total_child_rooms', []) if i and i.get('name1')]
        if room_numbers:
            room_numbers = ','.join(room_numbers)
        else:
            room_numbers = ''
        item.update({'end': item.start + timedelta(minutes=item.duration)})  # Use timedelta correctly
        item.update({'patient': item.patient + \
        '\n Start Time: ' + str(item.start) + \
        '\n Therapy Appointment ID: ' + item.name + '\n Practitioner:' + str(item.practitioner) + \
        '\n Therapy Type:' + str(item.therapy_type) + \
        '\n Room Number:' + str(room_numbers)})
    print ("\n data ::::After:::::::::", data)
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
