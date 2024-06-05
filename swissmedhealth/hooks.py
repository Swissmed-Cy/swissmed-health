from . import __version__ as app_version

app_name = "swissmedhealth"
app_title = "Swissmedhealth"
app_publisher = "KAINOTOMO PH LTD"
app_description = "Customizations for app.swissmedhealth.com"
app_email = "info@kainotomo.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/swissmedhealth/css/swissmedhealth.css"
# app_include_js = "/assets/swissmedhealth/js/swissmedhealth.js"

# include js, css files in header of web template
# web_include_css = "/assets/swissmedhealth/css/swissmedhealth.css"
# web_include_js = "/assets/swissmedhealth/js/swissmedhealth.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "swissmedhealth/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Customer": "public/js/customer.js",
    "Lead": "public/js/lead.js",
    "CRM Activities": "public/js/crm_activities.js",
    "Patient Appointment": "public/js/patient.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
doctype_calendar_js = {"Patient Appointment" : "public/js/patient_appointment_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "swissmedhealth.utils.jinja_methods",
#	"filters": "swissmedhealth.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "swissmedhealth.install.before_install"
# after_install = "swissmedhealth.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "swissmedhealth.uninstall.before_uninstall"
# after_uninstall = "swissmedhealth.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "swissmedhealth.utils.before_app_install"
# after_app_install = "swissmedhealth.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "swissmedhealth.utils.before_app_uninstall"
# after_app_uninstall = "swissmedhealth.utils.after_app_uninstall"

# After migrate
after_migrate = [
    "swissmedhealth.utils.after_migrate.set_default_print_format",
]

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "swissmedhealth.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
    "Lead": "swissmedhealth.swissmedhealth.hooks.lead.Lead"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Lead": {
        "after_insert": "swissmedhealth.swissmedhealth.hooks.lead.after_insert",
        "after_delete": "swissmedhealth.swissmedhealth.hooks.lead.after_delete",
    },
    "Customer": {
        "before_insert": "swissmedhealth.swissmedhealth.hooks.customer.before_insert",
    },
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"swissmedhealth.tasks.all"
#	],
#	"daily": [
#		"swissmedhealth.tasks.daily"
#	],
#	"hourly": [
#		"swissmedhealth.tasks.hourly"
#	],
#	"weekly": [
#		"swissmedhealth.tasks.weekly"
#	],
#	"monthly": [
#		"swissmedhealth.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "swissmedhealth.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "swissmedhealth.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "swissmedhealth.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["swissmedhealth.utils.before_request"]
# after_request = ["swissmedhealth.utils.after_request"]

# Job Events
# ----------
# before_job = ["swissmedhealth.utils.before_job"]
# after_job = ["swissmedhealth.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"swissmedhealth.auth.validate"
# ]

fixtures = [{
    "doctype": "Client Script",
        "filters": {
            "name": [ "in", ["Custom button patient appointment"] ]
            }
        },
    ]

fixtures = [
    {"dt": "Workspace", "filters": [["module", "=", "Healthcare"]]}
]