# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from healthcare.healthcare.doctype.therapy_session.therapy_session import TherapySession as OriginalTherapySession

import datetime

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, get_link_to_form, get_time, getdate

from healthcare.healthcare.doctype.healthcare_settings.healthcare_settings import (
	get_income_account,
	get_receivable_account,
)
from healthcare.healthcare.doctype.nursing_task.nursing_task import NursingTask
from healthcare.healthcare.doctype.service_request.service_request import (
	update_service_request_status,
)
from healthcare.healthcare.utils import validate_nursing_tasks


class CTherapySession(OriginalTherapySession):
	def validate(self):
		self.set_exercises_from_therapy_type()
		self.validate_duplicate()
		self.set_total_counts()

	def after_insert(self):
		if self.service_request:
			update_service_request_status(
				self.service_request, self.doctype, self.name, "completed-Request Status"
			)

		self.create_nursing_tasks(post_event=False)

	def on_update(self):
		if self.appointment:
			frappe.db.set_value("Patient Appointment", self.appointment, "status", "Closed")

	def on_cancel(self):
		if self.appointment:
			frappe.db.set_value("Patient Appointment", self.appointment, "status", "Open")
		if self.service_request:
			frappe.db.set_value("Service Request", self.service_request, "status", "active-Request Status")

		self.update_sessions_count_in_therapy_plan(on_cancel=True)

	# def validate_duplicate(self):
	# 	print ("\n self ::::CUSTOM::::::::", self.custom_total_chairs)
	# 	ch = []
	# 	for c_name in self.custom_total_chairs:
	# 		print ("\n self ::::111111::::::::", c_name.name1)
	# 		ch.append(c_name.name1)
	  
	# 	end_time = datetime.datetime.combine(
	# 		getdate(self.start_date), get_time(self.start_time)
	# 	) + datetime.timedelta(minutes=flt(self.duration))

	# 	overlaps = frappe.db.sql(
	# 		"""
	# 	select
	# 		name
	# 	from
	# 		`tabTherapy Session`
	# 	where
	# 		start_date=%s and name!=%s and docstatus!=2
	# 		and (practitioner=%s or patient=%s) and
	# 		((start_time<%s and start_time + INTERVAL duration MINUTE>%s) or
	# 		(start_time>%s and start_time<%s) or
	# 		(start_time=%s))
	# 	""",
	# 		(
	# 			self.start_date,
	# 			self.name,
	# 			self.practitioner,
	# 			self.patient,
	# 			self.start_time,
	# 			end_time.time(),
	# 			self.start_time,
	# 			end_time.time(),
	# 			self.start_time,
	# 		),
	# 	)
	# 	print ("\n overlaps :::::::::::::::", overlaps)
		
	# 	if overlaps:
	# 		overlapping_details = []
	# 		for i in overlaps:
	# 			session = frappe.get_doc('Therapy Session', i[0])
	# 			for chair in session.custom_total_chairs:
	# 				if chair.name1 in ch:
	# 					overlapping_details.append(session.name)
	# 					# break
	# 		overlapping_details = _("Therapy Session overlaps with {0}").format(
	# 			str(overlapping_details)
	# 		)
	# 		frappe.throw(overlapping_details, title=_("Therapy Sessions Overlapping"))
	# 	else:
	# 		print ("Please select another chair")

	# def validate_duplicate(self):
	#     # Print statement for debugging
	#     print("\n self ::::CUSTOM::::::::", self.custom_total_chairs)

	#     # Initialize an empty list to store chair names
	#     ch = []

	#     # Loop through custom_total_chairs field to collect chair names
	#     for chair in self.custom_total_chairs:
	#         print("\n self ::::111111::::::::", chair.name1)
	#         ch.append(chair.name1)
	  
	#     # Calculate the end time of the current session
	#     end_time = datetime.datetime.combine(getdate(self.start_date), get_time(self.start_time)) + datetime.timedelta(minutes=flt(self.duration))

	#     # Query to find overlapping sessions
	#     overlaps = frappe.db.sql(
	#         """
	#         SELECT name
	#         FROM `tabTherapy Session`
	#         WHERE
	#             start_date=%s AND name!=%s AND docstatus!=2
	#             AND (practitioner=%s OR patient=%s) 
	#             AND (
	#                 (start_time<%s AND ADDTIME(start_time, SEC_TO_TIME(duration*60))>%s) 
	#                 OR 
	#                 (start_time>%s AND start_time<%s) 
	#                 OR 
	#                 (start_time=%s)
	#             )
	#         """,
	#         (
	#             self.start_date,
	#             self.name,
	#             self.practitioner,
	#             self.patient,
	#             self.start_time,
	#             end_time.time(),
	#             self.start_time,
	#             end_time.time(),
	#             self.start_time,
	#         ),
	#     )

	#     # Print statement for debugging
	#     print("\n overlaps :::::::::::::::", overlaps)
		
	#     # If overlaps exist, check for overlapping chairs
	#     if overlaps:
	#         overlapping_details = []
	#         for session_name in overlaps:
	#             session = frappe.get_doc('Therapy Session', session_name[0])
	#             for chair in session.custom_total_chairs:
	#                 if chair.name1 in ch:
	#                     overlapping_details.append(session.name)
	#                     break  # Stop checking chairs once a match is found
			
	#         # Prepare error message if overlapping sessions found
	#         if overlapping_details:
	#             overlapping_details = _("Therapy Session overlaps : please choose another practitioner or chair with {0}").format(str(overlapping_details))
	#             frappe.throw(overlapping_details, title=_("Therapy Sessions Overlapping"))
		
	#     else:
	#         print("No overlapping sessions found. Please select another chair.")

	def validate_duplicate(self):
		# Print statement for debugging
		print("\n self ::::CUSTOM::::::::", self.custom_total_chairs)

		# Initialize an empty list to store chair names
		ch = []

		# Loop through custom_total_chairs field to collect chair names
		for chair in self.custom_total_chairs:
			print("\n self ::::111111::::::::", chair.name1)
			ch.append(chair.name1)

		# Calculate the end time of the current session
		end_time = datetime.datetime.combine(getdate(self.start_date), get_time(self.start_time)) + datetime.timedelta(minutes=flt(self.duration))

		# Query to find overlapping sessions
		overlaps = frappe.db.sql(
			"""
			SELECT name
			FROM `tabTherapy Session`
			WHERE
				start_date=%s AND name!=%s AND docstatus!=2
				AND (practitioner=%s OR patient=%s) 
				AND (
					(start_time<%s AND ADDTIME(start_time, SEC_TO_TIME(duration*60))>%s) 
					OR 
					(start_time>%s AND start_time<%s) 
					OR 
					(start_time=%s)
				)
			""",
			(
				self.start_date,
				self.name,
				self.practitioner,
				self.patient,
				self.start_time,
				end_time.time(),
				self.start_time,
				end_time.time(),
				self.start_time,
			),
		)

		# Print statement for debugging
		print("\n overlaps :::::::::::::::", overlaps)
		
		# If overlaps exist, check for overlapping chairs
		if overlaps:
			overlapping_details = []
			for session_name in overlaps:
				session = frappe.get_doc('Therapy Session', session_name[0])
				for chair in session.custom_total_chairs:
					if chair.name1 in ch:
						overlapping_details.append(session.name)
						break  # Stop checking chairs once a match is found
			
			# Prepare error message if overlapping sessions found
			if overlapping_details:
				overlapping_details_message = _("Therapy Session overlaps with the following sessions: {0}. Please choose another time or chair.").format(", ".join(overlapping_details))
				frappe.throw(overlapping_details_message, title=_("Therapy Sessions Overlapping"))
		
		# Additional check to ensure the same practitioner cannot book multiple sessions in the same time slot
		practitioner_overlaps = frappe.db.sql(
			"""
			SELECT name
			FROM `tabTherapy Session`
			WHERE
				start_date=%s AND name!=%s AND docstatus!=2
				AND practitioner=%s
				AND (
					(start_time<%s AND ADDTIME(start_time, SEC_TO_TIME(duration*60))>%s) 
					OR 
					(start_time>%s AND start_time<%s) 
					OR 
					(start_time=%s)
				)
			""",
			(
				self.start_date,
				self.name,
				self.practitioner,
				self.start_time,
				end_time.time(),
				self.start_time,
				end_time.time(),
				self.start_time,
			),
		)

		# If practitioner has overlapping sessions, throw an error
		if practitioner_overlaps:
			practitioner_overlaps_message = _("The practitioner has another session booked at the same time: {0}. Please choose another time or practitioner.").format(", ".join([p[0] for p in practitioner_overlaps]))
			frappe.throw(practitioner_overlaps_message, title=_("Practitioner Overlap"))

		else:
			print("No overlapping sessions found. Please select another chair.")




	def on_submit(self):
		validate_nursing_tasks(self)
		self.update_sessions_count_in_therapy_plan()

		if self.service_request:
			frappe.db.set_value("Service Request", self.service_request, "status", "Completed")

	def create_nursing_tasks(self, post_event=True):
		template = frappe.db.get_value("Therapy Type", self.therapy_type, "nursing_checklist_template")
		if template:
			NursingTask.create_nursing_tasks_from_template(
				template,
				self,
				start_time=frappe.utils.get_datetime(f"{self.start_date} {self.start_time}"),
				post_event=post_event,
			)

	def update_sessions_count_in_therapy_plan(self, on_cancel=False):
		if self.get('workflow_state') == "Completed":
			therapy_plan = frappe.get_doc("Therapy Plan", self.therapy_plan)
			for entry in therapy_plan.therapy_plan_details:
				if entry.therapy_type == self.therapy_type:
					if on_cancel:
						entry.sessions_completed -= 1
					else:
						entry.sessions_completed += 1
			therapy_plan.save()

	def set_total_counts(self):
		target_total = 0
		counts_completed = 0
		for entry in self.exercises:
			if entry.counts_target:
				target_total += entry.counts_target
			if entry.counts_completed:
				counts_completed += entry.counts_completed

		self.db_set("total_counts_targeted", target_total)
		self.db_set("total_counts_completed", counts_completed)

	def set_exercises_from_therapy_type(self):
		if self.therapy_type and not self.exercises:
			therapy_type_doc = frappe.get_cached_doc("Therapy Type", self.therapy_type)
			if therapy_type_doc.exercises:
				for exercise in therapy_type_doc.exercises:
					self.append(
						"exercises",
						(frappe.copy_doc(exercise)).as_dict(),
					)

	def before_insert(self):
		if self.service_request:
			therapy_session = frappe.db.exists(
				"Therapy Session",
				{"service_request": self.service_request, "docstatus": ["!=", 2]},
			)
			if therapy_session:
				frappe.throw(
					_("Therapy Session {0} already created from service request {1}").format(
						frappe.bold(get_link_to_form("Therapy Session", therapy_session)),
						frappe.bold(get_link_to_form("Service Request", self.service_request)),
					),
					title=_("Already Exist"),
				)


@frappe.whitelist()
def create_therapy_session(source_name, target_doc=None):
	def set_missing_values(source, target):
		therapy_type = frappe.get_doc("Therapy Type", source.therapy_type)
		target.exercises = therapy_type.exercises

	doc = get_mapped_doc(
		"Patient Appointment",
		source_name,
		{
			"Patient Appointment": {
				"doctype": "Therapy Session",
				"field_map": [
					["appointment", "name"],
					["patient", "patient"],
					["patient_age", "patient_age"],
					["gender", "patient_sex"],
					["therapy_type", "therapy_type"],
					["therapy_plan", "therapy_plan"],
					["practitioner", "practitioner"],
					["department", "department"],
					["start_date", "appointment_date"],
					["start_time", "appointment_time"],
					["service_unit", "service_unit"],
					["company", "company"],
					["invoiced", "invoiced"],
				],
			}
		},
		target_doc,
		set_missing_values,
	)

	return doc


@frappe.whitelist()
def invoice_therapy_session(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.customer = frappe.db.get_value("Patient", source.patient, "customer")
		target.due_date = getdate()
		target.debit_to = get_receivable_account(source.company)
		item = target.append("items", {})
		item = get_therapy_item(source, item)
		target.set_missing_values(for_validate=True)

	doc = get_mapped_doc(
		"Therapy Session",
		source_name,
		{
			"Therapy Session": {
				"doctype": "Sales Invoice",
				"field_map": [
					["patient", "patient"],
					["referring_practitioner", "practitioner"],
					["company", "company"],
					["due_date", "start_date"],
				],
			}
		},
		target_doc,
		set_missing_values,
	)

	return doc


def get_therapy_item(therapy, item):
	item.item_code = frappe.db.get_value("Therapy Type", therapy.therapy_type, "item")
	item.description = _("Therapy Session Charges: {0}").format(therapy.practitioner)
	item.income_account = get_income_account(therapy.practitioner, therapy.company)
	item.cost_center = frappe.get_cached_value("Company", therapy.company, "cost_center")
	item.rate = therapy.rate
	item.amount = therapy.rate
	item.qty = 1
	item.reference_dt = "Therapy Session"
	item.reference_dn = therapy.name
	return item
