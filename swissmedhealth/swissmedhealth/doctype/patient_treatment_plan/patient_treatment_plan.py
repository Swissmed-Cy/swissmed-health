# Copyright (c) 2024, KAINOTOMO PH LTD and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from datetime import datetime, timedelta

# class PatientTreatmentPlan(Document):
#     #pass

# 	def before_save(self):
# 	    print(":::::::::::::::::::11111111111111111111::::::::::",self)
# 	    if self.start_date and self.duration:
# 	        self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
# 	        duration_minutes = float(self.duration)


# 	        if not duration_minutes:
# 	            return

# 	        # Calculate the end date by adding the duration to the start date
# 	        end_date = self.start_date + timedelta(minutes=duration_minutes)

# 	        # Format the end date to MM-DD-YYYY HH:mm:ss
# 	        formatted_end_date = end_date
# 	        #.strftime("%d-%m-%Y %H:%M:%S")
# 	        self.end_date = formatted_end_date
	        
