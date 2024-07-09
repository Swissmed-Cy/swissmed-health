import frappe
from frappe import _


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
            parent = '{filters.get("therapy_type")}'
        ORDER BY
            name1
    """)

def validate(self, method):
    validate_bed_chairs(self)


def validate_bed_chairs(self):
    if self.custom_total_chairs and self.custom_total_beds:
        frappe.throw(_("Can not assign Bed and Chair at same time."))