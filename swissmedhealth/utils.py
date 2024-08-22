import frappe
from frappe.utils import add_to_date
from datetime import datetime, timedelta


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_available_units(doctype, txt, searchfield, start, page_len, filters):
    if not 'start_date' in filters:
        frappe.throw("Start Date is Missing")
    if not 'start_time' in filters:
        frappe.throw("Start Time is Missing")
    date_str = filters['start_date']
    time_str = filters['start_time']
    duration_minutes = filters['duration']
    date_time_str = f'{date_str} {time_str}'
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    duration = timedelta(minutes=duration_minutes)
    end_date_time_obj = date_time_obj + duration
    end_time_str = end_date_time_obj.strftime('%H:%M:%S')
    unit1 = frappe.db.sql('''select service_unit,start_time,duration from `tabTherapy Session` where start_date = '{0}' and
                 service_unit is not null and workflow_state in ("Scheduled","Arrived") and
                name != '{3}' and service_unit like %(txt)s '''.format(date_str, time_str, end_time_str,filters['name']),{
			"txt": "%{0}%".format(txt)
		},as_dict=1)
    res_unit = []
    for dict in unit1:
        start_time = dict["start_time"]
        end_time = dict["start_time"] + timedelta(minutes=dict["duration"])
        if (str(time_str) >=  str(start_time) and str(time_str) < str(end_time)) or (str(end_time_str) > str(start_time) and str(end_time_str) <= str(end_time)):
            res_unit.append(dict["service_unit"])
        
    print(res_unit)
    unit2 = frappe.db.sql('''select service_unit from `tabTherapy Type Service Units` where parenttype = "Therapy Type" 
                  and parent = "{0}" and service_unit like %(txt)s '''.format(filters['therapy_type']),{"txt": "%{0}%".format(txt)},as_dict=1)
    unit2 = [i["service_unit"] for i in unit2]
    print(unit2)
    result = list(set(list(set(unit2) - set(res_unit))+list(set(res_unit) - set(unit2))))
    print(result)
    if res_unit and not unit2:
        return (())
    if not len(result) or not len(result[0]):
        return (())
    return [[val,val] for val in result]

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_practitioner(doctype, txt, searchfield, start, page_len, filters):
    if not 'therapy_type' in filters:
        frappe.throw("Select Therapy Type first")
    practitioner = frappe.db.sql('''select p.practitioner as practitioner, h.practitioner_name as practitioner_name from `tabPractitioner Multiselect` as p join `tabHealthcare Practitioner` as h on p.practitioner = h.name where p.parenttype = "Therapy Type" 
                  and p.parent = "{0}" and h.practitioner_name like %(txt)s '''.format(filters['therapy_type']),{"txt": "%{0}%".format(txt)},as_dict=1)
    practitioner = [[i['practitioner'],i['practitioner_name']] for i in practitioner]
    if not len(practitioner) or not len(practitioner[0]):
        return (())
    return practitioner
