frappe.ready(function () {

	let params = new URLSearchParams(window.location.search);
	let email_id = params.get('email_id');
	if (email_id) {
		frappe.call('swissmedhealth.swissmedhealth.web_form.dental_history.dental_history.get_dental_history_details', { email_id: email_id }).then(r => {
			let doc = r.message;

			frappe.web_form.set_values(doc);
			frappe.web_form.is_new = false;
			frappe.web_form.doc.name = doc.name;
		});
	} else {
		// redirect to home page
		window.location.href = '/';
	}

	// bind events here
	$('.submit-btn').on('click', function (e) {
		// Prevent the default form submission
		e.preventDefault();

		// set custom_status to 'Documentation received'
		frappe.web_form.doc.custom_status = 'Documentation received';

		frappe.call('swissmedhealth.swissmedhealth.web_form.dental_history.dental_history.save', { doc: frappe.web_form.doc }).then(() => {
			let params = new URLSearchParams(window.location.search);
			let email_id = params.get('email_id');
			window.location.href = '../lead-step-4/new?email_id=' + encodeURIComponent(email_id);
		}).catch((err) => {
			frappe.msgprint({
				title: __('Error'),
				indicator: 'red',
				message: __('An error occurred while submitting your details. Please try again later.')
			});
		});
	});

})