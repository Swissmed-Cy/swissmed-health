import frappe
from frappe import _

def on_update_after_submit(self, method):
    if self.get('workflow_state') == "Completed":
        self.update_sessions_count_in_therapy_plan()

@frappe.whitelist()
def get_filterted_data(doctype, txt, searchfield, start, page_len, filters):
    if not filters.get("date") or not filters.get("therapy_type"):
        frappe.throw(_("Please mention mandatory fields first"))
    data = frappe.db.sql(
    f"""
        SELECT DISTINCT tcc.{filters.get("field")} AS name
        FROM `{filters.get("doc")}` AS tcc
        JOIN `tabTherapy Session` AS ts ON ts.name = tcc.parent
        WHERE ts.start_date = '{filters.get("date")}'
        AND (
            (CAST('{filters.get("time")}' AS time) < ts.start_time
            AND (ADDTIME(CAST('{filters.get("time")}' AS time), SEC_TO_TIME({filters.get("duration")} * 60)) BETWEEN ts.start_time AND ADDTIME(ts.start_time, SEC_TO_TIME(ts.duration * 60)) or ADDTIME(CAST('{filters.get("time")}' AS time), SEC_TO_TIME({filters.get("duration")} * 60)) > ADDTIME(ts.start_time, SEC_TO_TIME(ts.duration * 60))))
            OR
            (CAST('{filters.get("time")}' AS time) BETWEEN ts.start_time AND ADDTIME(ts.start_time, SEC_TO_TIME(ts.duration * 60)))
        )
        """,
        as_dict=1
    )

    lst = [row.name for row in data]

    condition = ""

    if lst:
        condition += f"""
            AND {filters.get("field")} not in ( {','.join('"' + row + '"' for row in lst)} )
            """

    if filters.get('doc') == 'tabTotals Beds Child' and filters.get('field', False) == 'totals_beds':
        condition += f"""
            AND totals_beds in (select name from `tabTotals Beds` where center_location = '{filters.get("custom_center_location")}')
        """

    if filters.get('doc') == 'tabTotal Child Chair' and filters.get('field', False) == 'name1':
        condition += f"""
            AND name1 in (select name1 from `tabTotal Chair` where center_location = '{filters.get("custom_center_location")}')
        """

    return_data = frappe.db.sql(
        f"""
            SELECT
                DISTINCT {filters.get("field")} as name, {filters.get("field")}
            FROM
                `{filters.get("doc")}`
            WHERE 
                parent = '{filters.get("therapy_type")}'
             {condition}
            ORDER BY
                {filters.get("field")}
        """)
    # frappe.throw(str(return_data))
    return return_data


@frappe.whitelist()
def get_filterted_rooms(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql(
    f"""
        SELECT
            DISTINCT name1 as name
        FROM
            `tabTotal child rooms`
        WHERE
            parent = '{filters.get("therapy_type")}' AND name1 in (select room_number from `tabRoom Number` where test = '{filters.get("custom_center_location")}')
        ORDER BY
            name1
    """)

def validate(self, method):
    validate_bed_chairs(self)


def validate_bed_chairs(self):
    if self.custom_total_chairs and self.custom_total_beds:
        frappe.throw(_("Can not assign Bed and Chair at same time."))


def validate_session(self, method):
    from datetime import datetime, timedelta

    therapy_sessions = frappe.db.sql(
        """select name,start_time,duration from `tabTherapy Session` where patient='{0}' and start_date="{1}"
                   and workflow_state in ("Scheduled", "Arrived") and name != '{2}' """.format(
            self.patient, self.start_date, self.name
        ),
        as_dict=1,
    )
    for dict in therapy_sessions:
        start_time = str(dict["start_time"])
        end_time = str(dict["start_time"] + timedelta(minutes=dict["duration"]))
        date_time_obj = datetime.strptime(str(self.start_time), "%H:%M:%S")
        duration = timedelta(minutes=self.duration)
        self_end_time = (date_time_obj + duration).time()
        if (
            str(self.start_time) >= str(start_time)
            and str(self.start_time) < str(end_time)
        ) or (
            str(self_end_time) > str(start_time) and str(self_end_time) <= str(end_time)
        ):
            frappe.throw("Therapy Session for this Patient is overlapping with {0}".format(dict["name"]))

    therapy_sessions = frappe.db.sql(
        """select name,start_time,duration from `tabTherapy Session` where practitioner='{0}' and start_date="{1}"
                   and workflow_state in ("Scheduled", "Arrived") and name != '{2}' """.format(
            self.practitioner, self.start_date, self.name
        ),
        as_dict=1,
    )
    for dict in therapy_sessions:
        start_time = str(dict["start_time"])
        if (str(self.start_time) == str(start_time)):
            frappe.throw(f"Therapy Session for this Practitioner is scheduled for {start_time}")
