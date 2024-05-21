frappe.ready(function () {

	let params = new URLSearchParams(window.location.search);
	let email_id = params.get('email_id');
	if (email_id) {
		frappe.call('swissmedhealth.swissmedhealth.web_form.medical_history.medical_history.get_lead_details', { email_id: email_id }).then(r => {
			let doc = r.message;

			frappe.web_form.set_values(doc);
			frappe.web_form.is_new = false;
			frappe.web_form.doc.name = doc.name;
		});
	}

	// bind events here
	frappe.web_form.after_save = () => {
		let email_id = frappe.web_form.doc.email_id;
		let href = '/lead-step-2/new?email_id=' + encodeURIComponent(email_id);
		// Get the redirect button with class name "new-btn" and set the href attribute
		$('.new-btn').attr('href', href);
		// Also change the text of the button to "Please complete your medical history here"
		$('.new-btn').text('Medical information Form');
	}

	$('.submit-btn').on('click', async function (e) {

		// Get the email from the URL
		let params = new URLSearchParams(window.location.search);
		let email_id = params.get('email_id');
		if (!email_id) {
			// Get the email_id from the submitted form
			email_id = frappe.web_form.doc.email_id;
			let r = await frappe.call('swissmedhealth.swissmedhealth.web_form.medical_history.medical_history.get_lead_details', { email_id: email_id, throw_error: false });
			if (r.message == undefined) {
				return;
			}
			frappe.web_form.doc.name = r.message.name;
			// Prevent the default form submission
			e.preventDefault();

			frappe.call('swissmedhealth.swissmedhealth.web_form.medical_history.medical_history.save', { doc: frappe.web_form.doc }).then(r => {
				let email_id = r.message.email_id;
				window.location.href = '../lead-step-2/new?email_id=' + encodeURIComponent(email_id);
			}).catch((err) => {
				frappe.msgprint({
					title: __('Error'),
					indicator: 'red',
					message: __('An error occurred while submitting your details. Please try again later.')
				});
			});
		} else {
			// Prevent the default form submission
			e.preventDefault();
			frappe.call('swissmedhealth.swissmedhealth.web_form.medical_history.medical_history.save', { doc: frappe.web_form.doc }).then(r => {
				let email_id = r.message.email_id;
				window.location.href = '../lead-step-2/new?email_id=' + encodeURIComponent(email_id);
			}).catch((err) => {
				frappe.msgprint({
					title: __('Error'),
					indicator: 'red',
					message: __('An error occurred while submitting your details. Please try again later.')
				});
			});
		}

	});

})