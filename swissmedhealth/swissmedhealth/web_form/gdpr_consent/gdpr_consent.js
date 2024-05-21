frappe.ready(function () {

	let params = new URLSearchParams(window.location.search);
	let email_id = params.get('email_id');
	if (email_id) {
		frappe.call('swissmedhealth.swissmedhealth.web_form.gdpr_consent.gdpr_consent.get_customer_consent_details', { email_id: email_id }).then(r => {
			let doc = r.message;
			
			// if (doc.acceptance_date) is empty set the current date
			if (!doc.acceptance_date) {
				doc.acceptance_date = frappe.datetime.nowdate();
			}

			// set the values in the form
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

		frappe.call('swissmedhealth.swissmedhealth.web_form.gdpr_consent.gdpr_consent.save', { doc: frappe.web_form.doc }).then(() => {
			frappe.msgprint({
				title: __('Success'),
				indicator: 'green',
				message: __('We have successfully received your medical history. A member of our professional team will be in touch with you shortly to discuss the next steps. Thank you for entrusting us with your healthcare needs.')
			});

			$('.web-form-container').hide();
		}).catch((err) => {
			frappe.msgprint({
				title: __('Error'),
				indicator: 'red',
				message: __('An error occurred while submitting your details. Please try again later.')
			});
		});
	});

})